import json
import math

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
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


def haversine_miles(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance in miles between two GPS points."""
    r_miles = 3958.8
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = (
        math.sin(d_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return r_miles * c


class ReviewListView(ListView):
    model = PubReview
    template_name = "reviews/index.html"
    context_object_name = "reviews"
    paginate_by = 12

    AMENITY_FILTERS = {
        "cask": "serves_cask_ale",
        "cobs": "serves_cobs_or_food",
        "garden": "has_beer_garden",
        "dogs": "is_dog_friendly",
        "sports": "shows_live_sports",
    }

    def _get_user_coords(self):
        lat_str = self.request.GET.get("lat", "").strip()
        lng_str = self.request.GET.get("lng", "").strip()
        if not lat_str or not lng_str:
            return None, None
        try:
            lat = float(lat_str)
            lng = float(lng_str)
            if -90.0 <= lat <= 90.0 and -180.0 <= lng <= 180.0:
                return lat, lng
        except ValueError:
            pass
        return None, None

    def get_queryset(self):
        queryset = (
            PubReview.objects.filter(status=PubReview.Status.PUBLISHED)
            .select_related("author", "category")
            .prefetch_related("comments__author")
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

        # Filter by Search Query (including What's on Tap / Pint Ordered!)
        search_q = self.request.GET.get("q", "").strip()
        if search_q:
            queryset = queryset.filter(
                Q(pub_name__icontains=search_q)
                | Q(title__icontains=search_q)
                | Q(content__icontains=search_q)
                | Q(address__icontains=search_q)
                | Q(postcode__icontains=search_q)
                | Q(pint_ordered__icontains=search_q)
                | Q(comments__pint_ordered__icontains=search_q)
            ).distinct()

        # Filter by Amenity Checkboxes
        for param, field_name in self.AMENITY_FILTERS.items():
            if self.request.GET.get(param) == "1":
                queryset = queryset.filter(**{field_name: True})

        user_lat, user_lng = self._get_user_coords()
        sort = self.request.GET.get("sort", "nearest")
        reviews_list = list(queryset)

        for r in reviews_list:
            r.is_reviewed = 1 if r.has_community_reviews else 0
            r.avg_score = r.overall_rating if r.is_reviewed else 0.0
            r.cached_avg_pint_price = r.avg_pint_price
            if (
                user_lat is not None
                and user_lng is not None
                and r.latitude is not None
                and r.longitude is not None
            ):
                r.distance_miles = round(
                    haversine_miles(user_lat, user_lng, r.latitude, r.longitude), 2
                )
            else:
                r.distance_miles = None

        if sort == "nearest":
            if user_lat is not None and user_lng is not None:
                # Closest pubs first (grouped into 0.1-mile proximity bands),
                # then best average rating within that proximity, then exact distance
                reviews_list.sort(
                    key=lambda r: (
                        0 if r.distance_miles is not None else 1,
                        round(r.distance_miles, 1) if r.distance_miles is not None else 9999.0,
                        -r.is_reviewed,
                        -r.avg_score,
                        r.distance_miles if r.distance_miles is not None else 9999.0,
                        -r.like_count,
                    )
                )
            else:
                # Without GPS yet, order by best average rating first
                reviews_list.sort(
                    key=lambda r: (
                        -r.is_reviewed,
                        -r.avg_score,
                        -r.like_count,
                        -r.created_on.timestamp(),
                    )
                )
        elif sort == "top_pint":
            # Best average rating first, then closest distance if GPS is active
            reviews_list.sort(
                key=lambda r: (
                    -r.is_reviewed,
                    -r.avg_score,
                    r.distance_miles if r.distance_miles is not None else 9999.0,
                    -r.like_count,
                    -r.created_on.timestamp(),
                )
            )
        elif sort == "cheapest_pint":
            # Lowest reported pint price (£) first, then highest rating
            reviews_list.sort(
                key=lambda r: (
                    0 if r.cached_avg_pint_price is not None else 1,
                    r.cached_avg_pint_price if r.cached_avg_pint_price is not None else 999.0,
                    -r.is_reviewed,
                    -r.avg_score,
                    r.distance_miles if r.distance_miles is not None else 9999.0,
                )
            )
        elif sort == "most_liked":
            reviews_list.sort(
                key=lambda r: (
                    -r.like_count,
                    -r.is_reviewed,
                    -r.avg_score,
                    r.distance_miles if r.distance_miles is not None else 9999.0,
                )
            )
        else:
            # newest
            reviews_list.sort(
                key=lambda r: (
                    -r.is_reviewed,
                    -r.created_on.timestamp(),
                )
            )

        return reviews_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        area_counts = dict(
            PubReview.objects.filter(status=PubReview.Status.PUBLISHED)
            .values_list("brum_area")
            .annotate(total=Count("id"))
        )
        context["brum_areas"] = [
            (code, f"{label} ({area_counts.get(code, 0)})")
            for code, label in PubReview.BrumArea.choices
        ]
        context["categories"] = Category.objects.all()
        context["selected_area"] = self.request.GET.get("area", "")
        context["selected_category"] = self.request.GET.get("category", "")
        context["selected_sort"] = self.request.GET.get("sort", "nearest")
        context["search_query"] = self.request.GET.get("q", "")
        user_lat, user_lng = self._get_user_coords()
        context["user_lat"] = user_lat if user_lat is not None else ""
        context["user_lng"] = user_lng if user_lng is not None else ""
        context["has_gps"] = user_lat is not None and user_lng is not None
        context["active_amenities"] = {
            key: self.request.GET.get(key) == "1" for key in self.AMENITY_FILTERS
        }
        query_params = self.request.GET.copy()
        query_params.pop("page", None)
        context["filter_querystring"] = query_params.urlencode()
        return context


class ReviewDetailView(DetailView):
    model = PubReview
    template_name = "reviews/review_detail.html"
    context_object_name = "review"

    def get_queryset(self):
        qs = PubReview.objects.select_related("author", "category").prefetch_related(
            "likes", "bookmarks", "comments__author"
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
        context["user_has_bookmarked"] = (
            self.request.user.is_authenticated
            and review.bookmarks.filter(id=self.request.user.id).exists()
        )
        context["star_range"] = range(1, 6)
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = PubReview
    form_class = PubReviewForm
    template_name = "reviews/review_form.html"

    def _get_source_pub(self):
        if hasattr(self, "_cached_source_pub"):
            return self._cached_source_pub
        pub_slug = self.request.GET.get("pub", "").strip()
        pub_name = self.request.GET.get("pub_name", "").strip()
        source = None
        if pub_slug:
            source = PubReview.objects.select_related("category").filter(slug=pub_slug).first()
        if not source and pub_name:
            qs = PubReview.objects.select_related("category").filter(pub_name__iexact=pub_name)
            brum_area = self.request.GET.get("brum_area", "").strip()
            if brum_area:
                qs = qs.filter(brum_area=brum_area)
            source = qs.first()
        self._cached_source_pub = source
        return source

    def get_initial(self):
        initial = super().get_initial()
        source_pub = self._get_source_pub()
        if source_pub:
            initial.update(
                {
                    "pub_name": source_pub.pub_name,
                    "brum_area": source_pub.brum_area,
                    "address": source_pub.address,
                    "postcode": source_pub.postcode,
                    "category": source_pub.category_id,
                    "price_point": source_pub.price_point,
                    "serves_cask_ale": source_pub.serves_cask_ale,
                    "serves_cobs_or_food": source_pub.serves_cobs_or_food,
                    "has_beer_garden": source_pub.has_beer_garden,
                    "is_dog_friendly": source_pub.is_dog_friendly,
                    "shows_live_sports": source_pub.shows_live_sports,
                    "featured_image": source_pub.featured_image,
                }
            )
        for field in ("pub_name", "brum_area", "address", "postcode", "category", "price_point"):
            val = self.request.GET.get(field)
            if val:
                initial[field] = val
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["source_pub"] = self._get_source_pub()
        all_pubs = PubReview.objects.select_related("category").values(
            "pub_name",
            "brum_area",
            "address",
            "postcode",
            "category_id",
            "price_point",
            "serves_cask_ale",
            "serves_cobs_or_food",
            "has_beer_garden",
            "is_dog_friendly",
            "shows_live_sports",
            "featured_image",
        )
        pub_catalog = {}
        for p in all_pubs:
            name_key = p["pub_name"].strip()
            if name_key not in pub_catalog:
                pub_catalog[name_key] = p
        context["pub_catalog_names"] = sorted(pub_catalog.keys())
        context["pub_directory_json"] = json.dumps(pub_catalog)
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        # Look up any existing record for this pub to preserve GPS coordinates & fallback image
        existing_pub = PubReview.objects.filter(
            pub_name__iexact=form.instance.pub_name.strip(),
            brum_area=form.instance.brum_area,
        ).first()
        if not existing_pub:
            existing_pub = PubReview.objects.filter(
                pub_name__iexact=form.instance.pub_name.strip()
            ).first()

        if existing_pub:
            if form.instance.latitude is None and existing_pub.latitude is not None:
                form.instance.latitude = existing_pub.latitude
            if form.instance.longitude is None and existing_pub.longitude is not None:
                form.instance.longitude = existing_pub.longitude
            if (
                not form.instance.uploaded_image
                and (
                    not form.instance.featured_image
                    or form.instance.featured_image == PubReview.DEFAULT_IMAGE_URL
                )
                and existing_pub.featured_image
            ):
                form.instance.featured_image = existing_pub.featured_image

        # Find any unreviewed directory placeholder(s) for this same pub so we can
        # move their comments, likes, and bookmarks onto the new review instead of losing them.
        placeholders = list(
            PubReview.objects.filter(
                author__username="pub_directory",
                pub_name__iexact=form.instance.pub_name.strip(),
                brum_area=form.instance.brum_area,
            )
        )
        with transaction.atomic():
            response = super().form_valid(form)
            for placeholder in placeholders:
                placeholder.comments.all().update(review=self.object)
                self.object.likes.add(*placeholder.likes.all())
                self.object.bookmarks.add(*placeholder.bookmarks.all())
                placeholder.delete()
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

    def handle_no_permission(self):
        messages.error(self.request, "Hold on! You can only delete your own pub reviews.")
        return super().handle_no_permission()

    def form_valid(self, form):
        review = self.get_object()
        pub_name = review.pub_name
        has_community_activity = (
            review.comments.exists()
            or review.likes.exists()
            or review.bookmarks.exists()
            or User.objects.filter(username="pub_directory").exists()
        )
        if has_community_activity:
            # Revert the pub back to an unreviewed Birmingham directory listing so
            # other users' comments, likes, bookmarks, and the pub entry are preserved.
            directory_user, created = User.objects.get_or_create(
                username="pub_directory",
                defaults={"email": "directory@secondcitypint.co.uk"},
            )
            if created:
                directory_user.set_unusable_password()
                directory_user.save()

            area_label = review.get_brum_area_display()
            base_title = f"{review.pub_name} — {area_label}"[:190]
            candidate_title = base_title
            counter = 2
            while PubReview.objects.filter(title=candidate_title).exclude(pk=review.pk).exists():
                candidate_title = f"{base_title} ({counter})"
                counter += 1

            cat_name = review.category.name if review.category else "Birmingham Pub"
            loc_str = (
                f" at {review.address}, {review.postcode}"
                if review.address and review.postcode
                else ""
            )
            review.author = directory_user
            review.title = candidate_title
            review.content = (
                f"{review.pub_name} is a {cat_name.lower()} in {area_label}{loc_str}. "
                f"Have you visited for a pint recently? Add your rating, pint price, and review below!"
            )
            review.excerpt = f"{cat_name} in {area_label}{loc_str}."[:220]
            review.pint_ordered = ""
            review.pint_price = None
            if review.uploaded_image:
                review.uploaded_image.delete(save=False)
                review.uploaded_image = None
            review.pint_quality_rating = 4
            review.atmosphere_rating = 4
            review.value_rating = 4
            review.status = PubReview.Status.PUBLISHED
            review.save()
            messages.warning(self.request, f"Your review of {pub_name} has been deleted.")
            return redirect(self.get_success_url())

        messages.warning(self.request, f"Your review of {pub_name} has been deleted.")
        return super().form_valid(form)


class LikeReviewView(LoginRequiredMixin, View):
    def post(self, request, slug):
        review = get_object_or_404(
            PubReview, slug=slug, status=PubReview.Status.PUBLISHED
        )
        if review.likes.filter(id=request.user.id).exists():
            review.likes.remove(request.user)
            messages.info(request, f"Removed your cheers from {review.pub_name}.")
        else:
            review.likes.add(request.user)
            messages.success(request, f"You raised a glass to {review.pub_name}! 🍻")
        return redirect(f"{reverse('reviews:detail', kwargs={'slug': slug})}#engagement-bar")


class ToggleBookmarkView(LoginRequiredMixin, View):
    def post(self, request, slug):
        review = get_object_or_404(
            PubReview, slug=slug, status=PubReview.Status.PUBLISHED
        )
        if review.bookmarks.filter(id=request.user.id).exists():
            review.bookmarks.remove(request.user)
            messages.info(
                request,
                f"Removed {review.pub_name} from your Pint Passport wishlist.",
            )
        else:
            review.bookmarks.add(request.user)
            messages.success(
                request,
                f"Saved {review.pub_name} to your 'Want to Visit' Pint Passport! 🗺️",
            )
        next_url = request.POST.get("next")
        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(next_url)
        return redirect(f"{reverse('reviews:detail', kwargs={'slug': slug})}#engagement-bar")


class MyPassportRedirectView(LoginRequiredMixin, View):
    def get(self, request):
        return redirect("reviews:passport", username=request.user.username)


class PintPassportView(DetailView):
    model = User
    template_name = "reviews/passport.html"
    context_object_name = "profile_user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_queryset(self):
        return User.objects.exclude(username="pub_directory")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.object
        is_own_passport = (
            self.request.user.is_authenticated and self.request.user == profile_user
        )

        base_qs = (
            PubReview.objects.select_related("author", "category")
            .prefetch_related("comments__author")
            .annotate(
                like_count=Count("likes", distinct=True),
                comment_count=Count(
                    "comments",
                    filter=Q(comments__approved=True),
                    distinct=True,
                ),
            )
        )

        published_reviews = (
            base_qs.filter(
                Q(author=profile_user) | Q(comments__author=profile_user, comments__approved=True),
                status=PubReview.Status.PUBLISHED,
            )
            .distinct()
            .order_by("-created_on")
        )

        user_comments = Comment.objects.filter(author=profile_user, approved=True)

        draft_reviews = (
            base_qs.filter(author=profile_user, status=PubReview.Status.DRAFT).order_by("-updated_on")
            if is_own_passport
            else PubReview.objects.none()
        )

        bookmarked_reviews = base_qs.filter(
            bookmarks=profile_user,
            status=PubReview.Status.PUBLISHED,
        ).order_by("-created_on")

        liked_reviews = base_qs.filter(
            likes=profile_user,
            status=PubReview.Status.PUBLISHED,
        ).order_by("-created_on")

        # Total cheers received on this user's own authored published reviews
        total_cheers_received = sum(
            r.like_count for r in published_reviews if r.author_id == profile_user.id
        )

        # Average Pint Quality rating given by this reviewer across main reviews & community reviews
        pint_scores = list(
            PubReview.objects.filter(
                author=profile_user, status=PubReview.Status.PUBLISHED
            ).values_list("pint_quality_rating", flat=True)
        ) + list(user_comments.values_list("pint_quality_rating", flat=True))
        avg_pint_rating = round(sum(pint_scores) / len(pint_scores), 1) if pint_scores else 0.0

        # District Stamps: stamped if user has reviewed OR cheered a pub in that Brum district
        reviewed_areas = set(published_reviews.values_list("brum_area", flat=True))
        liked_areas = set(liked_reviews.values_list("brum_area", flat=True))
        stamped_area_codes = reviewed_areas | liked_areas

        district_stamps = []
        for code, label in PubReview.BrumArea.choices:
            district_stamps.append(
                {
                    "code": code,
                    "label": label,
                    "stamped": code in stamped_area_codes,
                    "reviewed": code in reviewed_areas,
                }
            )

        # Earned Brummie Badges with Progress Tracking
        total_user_reviews = len(pint_scores)
        has_cask = (
            published_reviews.filter(serves_cask_ale=True).exists()
            or liked_reviews.filter(serves_cask_ale=True).exists()
        )
        has_cobs = (
            published_reviews.filter(serves_cobs_or_food=True).exists()
            or liked_reviews.filter(serves_cobs_or_food=True).exists()
        )
        logged_pint_prices = (
            PubReview.objects.filter(author=profile_user, pint_price__isnull=False).count()
            + user_comments.filter(pint_price__isnull=False).count()
        )
        uploaded_photos_count = (
            PubReview.objects.filter(author=profile_user)
            .exclude(uploaded_image="")
            .exclude(uploaded_image__isnull=True)
            .count()
            + user_comments.exclude(uploaded_image="").exclude(uploaded_image__isnull=True).count()
        )
        southside_areas = {
            PubReview.BrumArea.STIRCHLEY,
            PubReview.BrumArea.MOSELEY,
            PubReview.BrumArea.KINGS_HEATH,
        }
        central_areas = {
            PubReview.BrumArea.JEWELLERY_QUARTER,
            PubReview.BrumArea.DIGBETH,
            PubReview.BrumArea.CITY_CENTRE,
        }

        badges = [
            {
                "icon": "✍️",
                "title": "Second City Scribe",
                "description": "Published at least 1 Birmingham pub review",
                "earned": total_user_reviews >= 1,
                "progress_label": f"{min(total_user_reviews, 1)} / 1 review",
            },
            {
                "icon": "🍺",
                "title": "Cask Ale Connoisseur",
                "description": "Reviewed or cheered a proper hand-pulled cask boozer",
                "earned": has_cask,
                "progress_label": "Unlocked!" if has_cask else "0 / 1 cask pub",
            },
            {
                "icon": "💷",
                "title": "Pint Price Spotter",
                "description": "Logged the pint ordered & price paid (£) on a review",
                "earned": logged_pint_prices >= 1,
                "progress_label": f"{min(logged_pint_prices, 1)} / 1 pint price logged",
            },
            {
                "icon": "📸",
                "title": "Pint Photographer",
                "description": "Uploaded a real photo of a Birmingham pub or pint",
                "earned": uploaded_photos_count >= 1,
                "progress_label": f"{min(uploaded_photos_count, 1)} / 1 photo uploaded",
            },
            {
                "icon": "🗺️",
                "title": "Brum District Explorer",
                "description": "Stamped 3 or more Birmingham districts in the Pint Passport",
                "earned": len(stamped_area_codes) >= 3,
                "progress_label": f"{min(len(stamped_area_codes), 3)} / 3 districts",
            },
            {
                "icon": "👑",
                "title": "Lord Mayor of Brum",
                "description": "Stamped 8 or more of Birmingham's 32 districts",
                "earned": len(stamped_area_codes) >= 8,
                "progress_label": f"{min(len(stamped_area_codes), 8)} / 8 districts",
            },
            {
                "icon": "🏭",
                "title": "Southside & Beer Mile Hophead",
                "description": "Stamped Stirchley, Moseley, or Kings Heath",
                "earned": bool(stamped_area_codes & southside_areas),
                "progress_label": "Unlocked!" if (stamped_area_codes & southside_areas) else "Visit Stirchley / Moseley / KH",
            },
            {
                "icon": "💎",
                "title": "JQ, Digbeth & Central Regular",
                "description": "Stamped the Jewellery Quarter, Digbeth, or City Centre",
                "earned": bool(stamped_area_codes & central_areas),
                "progress_label": "Unlocked!" if (stamped_area_codes & central_areas) else "Visit JQ / Digbeth / Central",
            },
            {
                "icon": "🥪",
                "title": "Cob & Crust Loyalist",
                "description": "Backed a Birmingham pub serving classic crusty cobs or grub",
                "earned": has_cobs,
                "progress_label": "Unlocked!" if has_cobs else "0 / 1 food/cob pub",
            },
        ]

        context.update(
            {
                "is_own_passport": is_own_passport,
                "published_reviews": published_reviews,
                "draft_reviews": draft_reviews,
                "bookmarked_reviews": bookmarked_reviews,
                "liked_reviews": liked_reviews,
                "total_cheers_received": total_cheers_received,
                "avg_pint_rating": avg_pint_rating,
                "district_stamps": district_stamps,
                "stamped_count": len(stamped_area_codes),
                "total_districts": len(PubReview.BrumArea.choices),
                "badges": badges,
                "earned_badges_count": sum(1 for b in badges if b["earned"]),
            }
        )
        return context


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, slug):
        review = get_object_or_404(
            PubReview, slug=slug, status=PubReview.Status.PUBLISHED
        )
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review
            comment.author = request.user
            comment.save()
            messages.success(
                request,
                f"Cheers! Your review and {comment.overall_rating}/5 rating for {review.pub_name} have been added!",
            )
        else:
            messages.error(request, "Could not post your review. Please check the form fields.")
        return redirect(f"{reverse('reviews:detail', kwargs={'slug': slug})}#comments-section")


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get_comment(self):
        return get_object_or_404(Comment, pk=self.kwargs["pk"])

    def test_func(self):
        comment = self.get_comment()
        return self.request.user == comment.author or self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "Hold on! You can only delete your own comments.")
        return super().handle_no_permission()

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
