from django.urls import path
from .views import (
    ProfileDetailView,
    ProfileListView,
    UnFollowView,
    UpdateProfileView,
    FollowView,
    FollowerListView,
)


urlpatterns = [
    path("all/", ProfileListView.as_view(), name="all-profiles"),
    path("me/", ProfileDetailView.as_view(), name="my-profile"),
    path("me/update/", UpdateProfileView.as_view(), name="update-profile"),
    path("me/followers/", FollowerListView.as_view(), name="followers"),
    path("<uuid:user_id>/follow/", FollowView.as_view(), name="follow"),
    path("<uuid:user_id>/unfollow/", UnFollowView.as_view(), name="unfollow"),
]
