from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from reviews.views import RegisterView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/register/", RegisterView.as_view(), name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("reviews.urls", namespace="reviews")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
