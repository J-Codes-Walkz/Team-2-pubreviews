from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PubReview, Comment


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
            "price_point",
            "pint_quality_rating",
            "atmosphere_rating",
            "value_rating",
            "serves_cask_ale",
            "serves_cobs_or_food",
            "has_beer_garden",
            "is_dog_friendly",
            "shows_live_sports",
            "excerpt",
            "content",
            "featured_image",
            "status",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g., Unbeatable Bathams and Stained Glass Splendour",
                }
            ),
            "pub_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g., The Craven Arms"}
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
            "brum_area": forms.Select(attrs={"class": "form-select"}),
            "price_point": forms.Select(attrs={"class": "form-select"}),
            "excerpt": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "maxlength": "220",
                    "placeholder": "One-sentence hook for the homepage card (optional — auto-generated if blank)",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 7,
                    "placeholder": "Tell fellow Brummies about the pint, the cobs, the carpet, and the crowd...",
                }
            ),
            "featured_image": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://images.unsplash.com/...",
                }
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            "serves_cask_ale": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "serves_cobs_or_food": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "has_beer_garden": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_dog_friendly": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "shows_live_sports": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]
        labels = {"body": "Add your thoughts or pint recommendation"}
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Had a pint here recently? Share your thoughts on the tap list or cobs...",
                }
            )
        }


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
