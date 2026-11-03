from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import PubReviewForm, CommentForm, BrummieRegisterForm
from .models import PubReview, Category, Comment


class ReviewListView(ListView):
    model = PubReview
    template_name = "reviews/index.html"
    context_object_name = "reviews"
    paginate_by = 9

    AMENITY_FILTERS = {
        "cask": "serves_cask_ale",
        "cobs": "serves_cobs_or_food",
        "garden": "has_beer_garden",
        "dogs": "is_dog_friendly",
        "sports": "shows_live_sports",
    }

    def get_queryset(self):
        queryset = (
            PubReview.objects.filter(status=PubReview.Status.PUBLISHED)
            .select_related("author", "category")
            .annotate(
                like_count=Count("likes", distinct=True),
                comment_count=Count(
                    "comments",
                    filter=Q(comments__approved=True),
                    distinct=True,
                ),
            )
        )

        # Filter by Birmingham Area
        area = self.request.GET.get("area", "").strip()
        if area and area in dict(PubReview.BrumArea.choices):
            queryset = queryset.filter(brum_area=area)

        # Filter by Category
        category_slug = self.request.GET.get("category", "").strip()
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Filter by Search Query
        search_q = self.request.GET.get("q", "").strip()
        if search_q:
            queryset = queryset.filter(
                Q(pub_name__icontains=search_q)
                | Q(title__icontains=search_q)
                | Q(content__icontains=search_q)
            )

        # Filter by Amenity Checkboxes
        for param, field_name in self.AMENITY_FILTERS.items():
            if self.request.GET.get(param) == "1":
                queryset = queryset.filter(**{field_name: True})

        # Sorting
        sort = self.request.GET.get("sort", "newest")
        if sort == "top_pint":
            queryset = queryset.order_by("-pint_quality_rating", "-like_count", "-created_on")
        elif sort == "most_liked":
            queryset = queryset.order_by("-like_count", "-created_on")
        else:
            queryset = queryset.order_by("-created_on")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["brum_areas"] = PubReview.BrumArea.choices
        context["categories"] = Category.objects.all()
        context["selected_area"] = self.request.GET.get("area", "")
        context["selected_category"] = self.request.GET.get("category", "")
        context["selected_sort"] = self.request.GET.get("sort", "newest")
        context["search_query"] = self.request.GET.get("q", "")
        context["active_amenities"] = {
            key: self.request.GET.get(key) == "1" for key in self.AMENITY_FILTERS
        }
        return context


class ReviewDetailView(DetailView):
    model = PubReview
    template_name = "reviews/review_detail.html"
    context_object_name = "review"

    def get_queryset(self):
        qs = PubReview.objects.select_related("author", "category").prefetch_related(
            "likes", "comments__author"
        )
        if self.request.user.is_authenticated:
            return qs.filter(
                Q(status=PubReview.Status.PUBLISHED) | Q(author=self.request.user)
            )
        return qs.filter(status=PubReview.Status.PUBLISHED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review = self.object
        context["comments"] = review.comments.filter(approved=True).select_related("author")
        context["comment_form"] = CommentForm()
        context["user_has_liked"] = (
            self.request.user.is_authenticated
            and review.likes.filter(id=self.request.user.id).exists()
        )
        context["star_range"] = range(1, 6)
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = PubReview
    form_class = PubReviewForm
    template_name = "reviews/review_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Cheers! Your review of {self.object.pub_name} has been posted.",
        )
        return response


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PubReview
    form_class = PubReviewForm
    template_name = "reviews/review_form.html"

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.author

    def handle_no_permission(self):
        messages.error(self.request, "Hold on! You can only edit your own pub reviews.")
        return super().handle_no_permission()

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Updated your review for {self.object.pub_name}.",
        )
        return response


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PubReview
    template_name = "reviews/review_confirm_delete.html"
    success_url = reverse_lazy("reviews:index")

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.author

    def form_valid(self, form):
        pub_name = self.get_object().pub_name
        messages.warning(self.request, f"Your review of {pub_name} has been deleted.")
        return super().form_valid(form)


class LikeReviewView(LoginRequiredMixin, View):
    def post(self, request, slug):
        review = get_object_or_404(PubReview, slug=slug)
        if review.likes.filter(id=request.user.id).exists():
            review.likes.remove(request.user)
            messages.info(request, f"Removed your cheers from {review.pub_name}.")
        else:
            review.likes.add(request.user)
            messages.success(request, f"You raised a glass to {review.pub_name}! 🍻")
        return redirect(f"{reverse('reviews:detail', kwargs={'slug': slug})}#engagement-bar")


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, slug):
        review = get_object_or_404(PubReview, slug=slug)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review
            comment.author = request.user
            comment.save()
            messages.success(request, "Your comment has been added to the bar tab!")
        else:
            messages.error(request, "Could not post your comment. Please check the form.")
        return redirect(f"{reverse('reviews:detail', kwargs={'slug': slug})}#comments-section")


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get_comment(self):
        return get_object_or_404(Comment, pk=self.kwargs["pk"])

    def test_func(self):
        comment = self.get_comment()
        return self.request.user == comment.author or self.request.user.is_staff

    def post(self, request, pk):
        comment = self.get_comment()
        review_slug = comment.review.slug
        comment.delete()
        messages.warning(request, "Your comment was removed.")
        return redirect(f"{reverse('reviews:detail', kwargs={'slug': review_slug})}#comments-section")


class RegisterView(CreateView):
    form_class = BrummieRegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("reviews:index")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(
            self.request,
            f"Welcome to The Second City Pint, {self.object.username}! Grab a stool.",
        )
        return response
