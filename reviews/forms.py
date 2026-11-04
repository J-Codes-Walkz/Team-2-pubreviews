from decimal import Decimal
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import PubReview, Comment


MAX_UPLOAD_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


def validate_uploaded_image_file(uploaded_file):
    """Verify file size and actual binary magic bytes for uploaded images."""
    if not uploaded_file:
        return uploaded_file

    if getattr(uploaded_file, "size", 0) > MAX_UPLOAD_SIZE_BYTES:
        raise ValidationError("Image file size must be under 5 MB.")

    # Only inspect magic bytes when a new file is being uploaded
    if hasattr(uploaded_file, "read") and hasattr(uploaded_file, "seek"):
        try:
            pos = uploaded_file.tell() if hasattr(uploaded_file, "tell") else 0
            header = uploaded_file.read(16)
            uploaded_file.seek(pos)
        except Exception:
            header = b""

        if header:
            is_jpeg = header.startswith(b"\xff\xd8\xff")
            is_png = header.startswith(b"\x89PNG\r\n\x1a\n")
            is_gif = header.startswith((b"GIF87a", b"GIF89a"))
            is_webp = len(header) >= 12 and header[:4] == b"RIFF" and header[8:12] == b"WEBP"
            if not (is_jpeg or is_png or is_gif or is_webp):
                raise ValidationError(
                    "Uploaded file is not a valid image (must be JPEG, PNG, WEBP, or GIF)."
                )
    return uploaded_file


class PubReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, f"{i} / 5") for i in range(1, 6)]

    pint_quality_rating = forms.TypedChoiceField(
        choices=RATING_CHOICES,
        coerce=int,
        initial=5,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Pint Quality (Keep, Temperature & Head)",
    )
    atmosphere_rating = forms.TypedChoiceField(
        choices=RATING_CHOICES,
        coerce=int,
        initial=5,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Atmosphere & Decor",
    )
    value_rating = forms.TypedChoiceField(
        choices=RATING_CHOICES,
        coerce=int,
        initial=4,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Value for Money",
    )

    class Meta:
        model = PubReview
        fields = [
            "title",
            "pub_name",
            "category",
            "brum_area",
            "address",
            "postcode",
            "price_point",
            "pint_quality_rating",
            "atmosphere_rating",
            "value_rating",
            "pint_ordered",
            "pint_price",
            "serves_cask_ale",
            "serves_cobs_or_food",
            "has_beer_garden",
            "is_dog_friendly",
            "shows_live_sports",
            "excerpt",
            "content",
            "uploaded_image",
            "featured_image",
            "status",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., Cracking Pint of Bathams and Friendly Regulars",
                }
            ),
            "pub_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Start typing a Birmingham pub name (e.g., The Craven Arms)...",
                    "list": "birmingham-pubs-datalist",
                    "autocomplete": "off",
                }
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
            "brum_area": forms.Select(attrs={"class": "form-select"}),
            "address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g., 75-77 Upper Dean St"}
            ),
            "postcode": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g., B5 4SG"}
            ),
            "price_point": forms.Select(attrs={"class": "form-select"}),
            "pint_ordered": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., Bathams Best Bitter, Attic Intuition, Guinness",
                }
            ),
            "pint_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.05",
                    "min": "1.00",
                    "max": "25.00",
                    "placeholder": "e.g., 4.50",
                }
            ),
            "excerpt": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": "220",
                    "placeholder": "One-sentence summary for the pub card (optional — auto-generated if left blank)",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Tell fellow Brummies about the pint quality, atmosphere, price, and cobs...",
                }
            ),
            "uploaded_image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
            "featured_image": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://... (optional if uploading a photo above)",
                }
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            "serves_cask_ale": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "serves_cobs_or_food": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "has_beer_garden": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_dog_friendly": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "shows_live_sports": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_uploaded_image(self):
        return validate_uploaded_image_file(self.cleaned_data.get("uploaded_image"))

    def clean_pint_price(self):
        price = self.cleaned_data.get("pint_price")
        if price is not None and (price < Decimal("1.00") or price > Decimal("25.00")):
            raise ValidationError("Pint price must be between £1.00 and £25.00.")
        return price

    def clean_featured_image(self):
        url = (self.cleaned_data.get("featured_image") or "").strip()
        if url and not url.lower().startswith(("http://", "https://")):
            raise ValidationError("Image URL must start with http:// or https://.")
        return url


class CommentForm(forms.ModelForm):
    RATING_CHOICES = [(i, f"{i} / 5 ⭐") for i in range(5, 0, -1)]

    pint_quality_rating = forms.TypedChoiceField(
        choices=RATING_CHOICES,
        coerce=int,
        initial=5,
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
        label="🍺 Pint Quality",
    )
    atmosphere_rating = forms.TypedChoiceField(
        choices=RATING_CHOICES,
        coerce=int,
        initial=5,
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
        label="🔥 Atmosphere",
    )
    value_rating = forms.TypedChoiceField(
        choices=RATING_CHOICES,
        coerce=int,
        initial=4,
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
        label="💷 Value",
    )

    class Meta:
        model = Comment
        fields = [
            "pint_quality_rating",
            "atmosphere_rating",
            "value_rating",
            "pint_ordered",
            "pint_price",
            "uploaded_image",
            "body",
        ]
        labels = {
            "body": "Your Review & Pint Notes *",
            "pint_ordered": "🍺 Pint Ordered (What's on Tap?)",
            "pint_price": "💷 Price Paid (£)",
            "uploaded_image": "📸 Upload a Photo of Your Pint or the Pub",
        }
        widgets = {
            "pint_ordered": forms.TextInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "placeholder": "e.g., Bathams Best Bitter, Intuition Pale, Guinness...",
                }
            ),
            "pint_price": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "step": "0.05",
                    "min": "1.00",
                    "max": "25.00",
                    "placeholder": "e.g., 4.50",
                }
            ),
            "uploaded_image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control form-control-sm",
                    "accept": "image/*",
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Share how the pint kept, what's on the hand-pulls, the cobs, and the vibe...",
                }
            ),
        }

    def clean_uploaded_image(self):
        return validate_uploaded_image_file(self.cleaned_data.get("uploaded_image"))

    def clean_pint_price(self):
        price = self.cleaned_data.get("pint_price")
        if price is not None and (price < Decimal("1.00") or price > Decimal("25.00")):
            raise ValidationError("Pint price must be between £1.00 and £25.00.")
        return price


class BrummieRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.co.uk"}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
