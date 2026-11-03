from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True, blank=True)
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class PubReview(models.Model):
    class BrumArea(models.TextChoices):
        CITY_CENTRE = "CITY_CENTRE", "City Centre"
        DIGBETH = "DIGBETH", "Digbeth"
        JEWELLERY_QUARTER = "JEWELLERY_QUARTER", "Jewellery Quarter"
        HARBORNE = "HARBORNE", "Harborne"
        MOSELEY = "MOSELEY", "Moseley"
        STIRCHLEY = "STIRCHLEY", "Stirchley"
        KINGS_HEATH = "KINGS_HEATH", "Kings Heath"
        ASTON = "ASTON", "Aston"
        EDGBASTON = "EDGBASTON", "Edgbaston"
        BOURNVILLE = "BOURNVILLE", "Bournville"

    class PricePoint(models.TextChoices):
        BARGAIN = "£", "£ (Bargain pint)"
        STANDARD = "££", "££ (Standard boozer)"
        PREMIUM = "£££", "£££ (Premium / Craft)"

    class Status(models.IntegerChoices):
        DRAFT = 0, "Draft"
        PUBLISHED = 1, "Published"

    DEFAULT_IMAGE_URL = (
        "https://images.unsplash.com/photo-1514933651103-005eec06c04b"
        "?auto=format&fit=crop&w=1200&q=80"
    )

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    pub_name = models.CharField(max_length=150)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviews",
    )
    brum_area = models.CharField(
        max_length=30,
        choices=BrumArea.choices,
        default=BrumArea.CITY_CENTRE,
        db_index=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pub_reviews",
    )
    price_point = models.CharField(
        max_length=5,
        choices=PricePoint.choices,
        default=PricePoint.STANDARD,
    )

    # Amenities
    has_beer_garden = models.BooleanField("Beer Garden", default=False)
    is_dog_friendly = models.BooleanField("Dog Friendly", default=False)
    shows_live_sports = models.BooleanField("Live Sports", default=False)
    serves_cask_ale = models.BooleanField("Real Cask Ale", default=False)
    serves_cobs_or_food = models.BooleanField("Cobs / Pub Grub", default=False)

    # Ratings (1-5)
    pint_quality_rating = models.PositiveSmallIntegerField(
        default=4,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    atmosphere_rating = models.PositiveSmallIntegerField(
        default=4,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    value_rating = models.PositiveSmallIntegerField(
        default=4,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )

    content = models.TextField(help_text="Share the full story of your visit, the keep of the ale, and the vibe.")
    excerpt = models.CharField(
        max_length=220,
        blank=True,
        help_text="Short summary (max 220 chars) shown on review cards.",
    )
    featured_image = models.URLField(
        max_length=500,
        blank=True,
        default=DEFAULT_IMAGE_URL,
        help_text="Direct URL to a photo of the pub or pint (leave blank for default pub image).",
    )
    status = models.IntegerField(
        choices=Status.choices,
        default=Status.PUBLISHED,
        db_index=True,
    )
    likes = models.ManyToManyField(
        User,
        related_name="review_likes",
        blank=True,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.pub_name}-{self.title}")[:200]
            slug_candidate = base_slug
            counter = 1
            while PubReview.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
                slug_candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug_candidate

        if not self.featured_image:
            self.featured_image = self.DEFAULT_IMAGE_URL

        if not self.excerpt and self.content:
            plain = " ".join(self.content.split())
            self.excerpt = (plain[:217] + "...") if len(plain) > 220 else plain

        super().save(*args, **kwargs)

    @property
    def overall_rating(self):
        return round(
            (self.pint_quality_rating + self.atmosphere_rating + self.value_rating) / 3,
            1,
        )

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def image_url(self):
        return self.featured_image or self.DEFAULT_IMAGE_URL

    def get_absolute_url(self):
        return reverse("reviews:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.pub_name} ({self.get_brum_area_display()}) — {self.title}"


class Comment(models.Model):
    review = models.ForeignKey(
        PubReview,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="pub_comments",
    )
    body = models.TextField(max_length=1000)
    approved = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment by {self.author.username} on {self.review.pub_name}"
