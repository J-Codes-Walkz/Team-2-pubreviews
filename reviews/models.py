from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    FileExtensionValidator,
    URLValidator,
)
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
        DIGBETH = "DIGBETH", "Digbeth & Deritend"
        JEWELLERY_QUARTER = "JEWELLERY_QUARTER", "Jewellery Quarter & Hockley"
        BRINDLEYPLACE = "BRINDLEYPLACE", "Brindleyplace & Broad Street"
        CHINATOWN_GAY_VILLAGE = "CHINATOWN_GAY_VILLAGE", "Chinatown, Gay Village & Southside"
        GUN_QUARTER = "GUN_QUARTER", "Gun Quarter & Snow Hill"
        HARBORNE = "HARBORNE", "Harborne"
        MOSELEY = "MOSELEY", "Moseley"
        STIRCHLEY = "STIRCHLEY", "Stirchley"
        KINGS_HEATH = "KINGS_HEATH", "Kings Heath"
        EDGBASTON = "EDGBASTON", "Edgbaston"
        SELLY_OAK = "SELLY_OAK", "Selly Oak"
        BOURNVILLE = "BOURNVILLE", "Bournville & Cotteridge"
        ASTON = "ASTON", "Aston & Witton"
        SUTTON_COLDFIELD = "SUTTON_COLDFIELD", "Sutton Coldfield"
        ERDINGTON = "ERDINGTON", "Erdington"
        NORTHFIELD = "NORTHFIELD", "Northfield"
        KINGS_NORTON = "KINGS_NORTON", "Kings Norton"
        LONGBRIDGE_RUBERY = "LONGBRIDGE_RUBERY", "Longbridge, Rednal & Rubery"
        QUINTON = "QUINTON", "Quinton, Bartley Green & Woodgate"
        LADYWOOD = "LADYWOOD", "Ladywood & Five Ways"
        HANDSWORTH = "HANDSWORTH", "Handsworth & Lozells"
        PERRY_BARR = "PERRY_BARR", "Perry Barr, Great Barr & Kingstanding"
        BALSALL_HEATH = "BALSALL_HEATH", "Balsall Heath & Highgate"
        SPARKHILL = "SPARKHILL", "Sparkhill, Sparkbrook & Tyseley"
        HALL_GREEN = "HALL_GREEN", "Hall Green"
        ACOCKS_GREEN = "ACOCKS_GREEN", "Acocks Green"
        SHELDON_YARDLEY = "SHELDON_YARDLEY", "Sheldon, Yardley & Stechford"
        CASTLE_BROMWICH = "CASTLE_BROMWICH", "Castle Bromwich, Hodge Hill & Shard End"
        BORDESLEY_GREEN = "BORDESLEY_GREEN", "Bordesley Green & Small Heath"
        ALUM_ROCK = "ALUM_ROCK", "Alum Rock & Saltley"
        NECHELLS = "NECHELLS", "Nechells & Duddeston"

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
    address = models.CharField(
        max_length=200,
        blank=True,
        help_text="Street address in Birmingham (e.g., 75-77 Upper Dean St)",
    )
    postcode = models.CharField(
        max_length=20,
        blank=True,
        help_text="Birmingham postcode (e.g., B5 4SG)",
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
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

    # What's On Tap & Pint Price Tracker
    pint_ordered = models.CharField(
        "Pint Ordered (On Tap)",
        max_length=100,
        blank=True,
        help_text="e.g., Bathams Best Bitter, Attic Intuition Pale, Guinness",
    )
    pint_price = models.DecimalField(
        "Price Paid (£)",
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(Decimal("1.00")),
            MaxValueValidator(Decimal("25.00")),
        ],
        help_text="Price paid for a pint in £ (e.g., 4.50)",
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
        validators=[URLValidator(schemes=["http", "https"])],
        help_text="Direct URL to a photo of the pub or pint (leave blank for default pub image).",
    )
    uploaded_image = models.FileField(
        "Upload a Photo",
        upload_to="pub_photos/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "webp", "gif"]
            )
        ],
        help_text="Upload your own photo of the pub or your pint (JPG, PNG, WEBP, GIF).",
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
    bookmarks = models.ManyToManyField(
        User,
        related_name="bookmarked_reviews",
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

    def _get_approved_comments(self):
        if "_prefetched_objects_cache" in self.__dict__ and "comments" in self._prefetched_objects_cache:
            return [c for c in self._prefetched_objects_cache["comments"] if c.approved]
        return list(self.comments.filter(approved=True).select_related("author"))

    @property
    def has_community_reviews(self):
        if self.author.username != "pub_directory":
            return True
        return len(self._get_approved_comments()) > 0

    @property
    def community_review_count(self):
        base = 1 if self.author.username != "pub_directory" else 0
        return base + len(self._get_approved_comments())

    @property
    def avg_pint_quality(self):
        scores = []
        if self.author.username != "pub_directory":
            scores.append(self.pint_quality_rating)
        for c in self._get_approved_comments():
            if c.pint_quality_rating:
                scores.append(c.pint_quality_rating)
        return round(sum(scores) / len(scores), 1) if scores else float(self.pint_quality_rating)

    @property
    def avg_atmosphere(self):
        scores = []
        if self.author.username != "pub_directory":
            scores.append(self.atmosphere_rating)
        for c in self._get_approved_comments():
            if c.atmosphere_rating:
                scores.append(c.atmosphere_rating)
        return round(sum(scores) / len(scores), 1) if scores else float(self.atmosphere_rating)

    @property
    def avg_value(self):
        scores = []
        if self.author.username != "pub_directory":
            scores.append(self.value_rating)
        for c in self._get_approved_comments():
            if c.value_rating:
                scores.append(c.value_rating)
        return round(sum(scores) / len(scores), 1) if scores else float(self.value_rating)

    @property
    def overall_rating(self):
        scores = []
        if self.author.username != "pub_directory":
            scores.append(
                (self.pint_quality_rating + self.atmosphere_rating + self.value_rating) / 3.0
            )
        for c in self._get_approved_comments():
            if c.pint_quality_rating and c.atmosphere_rating and c.value_rating:
                scores.append(
                    (c.pint_quality_rating + c.atmosphere_rating + c.value_rating) / 3.0
                )
        if not scores:
            return round(
                (self.pint_quality_rating + self.atmosphere_rating + self.value_rating) / 3.0,
                1,
            )
        return round(sum(scores) / len(scores), 1)

    @property
    def avg_pint_price(self):
        prices = []
        if self.pint_price is not None:
            prices.append(float(self.pint_price))
        for c in self._get_approved_comments():
            if c.pint_price is not None:
                prices.append(float(c.pint_price))
        return round(sum(prices) / len(prices), 2) if prices else None

    @property
    def reported_pints(self):
        items = []
        if self.pint_ordered or self.pint_price is not None:
            items.append(
                {
                    "pint": self.pint_ordered or "House Pint",
                    "price": self.pint_price,
                    "author": self.author.username,
                    "date": self.created_on,
                }
            )
        for c in self._get_approved_comments():
            if c.pint_ordered or c.pint_price is not None:
                items.append(
                    {
                        "pint": c.pint_ordered or "House Pint",
                        "price": c.pint_price,
                        "author": c.author.username,
                        "date": c.created_on,
                    }
                )
        return items

    @property
    def gallery_photos(self):
        photos = []
        if self.uploaded_image:
            try:
                photos.append(
                    {
                        "url": self.uploaded_image.url,
                        "author": self.author.username,
                        "caption": self.pint_ordered or self.title,
                        "date": self.created_on,
                    }
                )
            except ValueError:
                pass
        for c in self._get_approved_comments():
            if c.uploaded_image:
                try:
                    photos.append(
                        {
                            "url": c.uploaded_image.url,
                            "author": c.author.username,
                            "caption": c.pint_ordered or c.body[:60],
                            "date": c.created_on,
                        }
                    )
                except ValueError:
                    pass
        return photos

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_bookmarks(self):
        return self.bookmarks.count()

    @property
    def image_url(self):
        return self.featured_image or self.DEFAULT_IMAGE_URL

    @property
    def card_image_url(self):
        url = self.image_url
        if "images.unsplash.com/" in url:
            return (
                url.replace("w=1200&q=80", "w=500&q=75&fm=webp")
                .replace("w=1600&q=80", "w=500&q=75&fm=webp")
            )
        prefix = "https://upload.wikimedia.org/wikipedia/commons/"
        if url.startswith(prefix) and "/thumb/" not in url:
            rest = url[len(prefix):]
            parts = rest.split("/")
            if len(parts) == 3 and parts[2].lower().endswith((".jpg", ".jpeg", ".png")):
                filename = parts[2]
                return f"{prefix}thumb/{rest}/500px-{filename}"
        return url

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
    pint_quality_rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    atmosphere_rating = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    value_rating = models.PositiveSmallIntegerField(
        default=4,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    pint_ordered = models.CharField(
        "Pint Ordered (Optional)",
        max_length=100,
        blank=True,
    )
    pint_price = models.DecimalField(
        "Price Paid (£)",
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(Decimal("1.00")),
            MaxValueValidator(Decimal("25.00")),
        ],
    )
    uploaded_image = models.FileField(
        "Upload a Photo (Optional)",
        upload_to="pub_photos/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "webp", "gif"]
            )
        ],
    )
    body = models.TextField(max_length=1000)
    approved = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    @property
    def overall_rating(self):
        return round(
            (self.pint_quality_rating + self.atmosphere_rating + self.value_rating) / 3.0,
            1,
        )

    def __str__(self):
        return f"Review by {self.author.username} on {self.review.pub_name}"
