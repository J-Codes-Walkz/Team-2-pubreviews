from django.contrib import admin
from .models import Category, PubReview, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ("created_on",)


@admin.register(PubReview)
class PubReviewAdmin(admin.ModelAdmin):
    list_display = (
        "pub_name",
        "title",
        "brum_area",
        "category",
        "price_point",
        "pint_quality_rating",
        "author",
        "status",
        "created_on",
    )
    list_filter = (
        "status",
        "brum_area",
        "category",
        "price_point",
        "serves_cask_ale",
        "has_beer_garden",
        "is_dog_friendly",
        "serves_cobs_or_food",
    )
    search_fields = ("pub_name", "title", "content", "author__username")
    prepopulated_fields = {"slug": ("pub_name", "title")}
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "review", "approved", "created_on")
    list_filter = ("approved", "created_on")
    search_fields = ("author__username", "body", "review__pub_name")
    actions = ["approve_comments"]

    @admin.action(description="Approve selected comments")
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
