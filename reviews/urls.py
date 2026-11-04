from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("", views.ReviewListView.as_view(), name="index"),
    path("passport/", views.MyPassportRedirectView.as_view(), name="my_passport"),
    path("passport/<str:username>/", views.PintPassportView.as_view(), name="passport"),
    path("review/new/", views.ReviewCreateView.as_view(), name="create"),
    path("review/<slug:slug>/", views.ReviewDetailView.as_view(), name="detail"),
    path("review/<slug:slug>/edit/", views.ReviewUpdateView.as_view(), name="edit"),
    path("review/<slug:slug>/delete/", views.ReviewDeleteView.as_view(), name="delete"),
    path("review/<slug:slug>/like/", views.LikeReviewView.as_view(), name="like"),
    path("review/<slug:slug>/bookmark/", views.ToggleBookmarkView.as_view(), name="bookmark"),
    path("review/<slug:slug>/comment/", views.CommentCreateView.as_view(), name="add_comment"),
    path("comment/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="delete_comment"),
]
