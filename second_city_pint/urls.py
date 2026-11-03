from django.contrib import admin
from django.urls import path, include
from reviews.views import RegisterView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("reviews.urls", namespace="reviews")),
]
