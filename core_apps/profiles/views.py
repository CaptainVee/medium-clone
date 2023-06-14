# TODO change this in production
from medium_clone.settings.local import DEFAULT_FROM_EMAIL
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from .exceptions import CantFollowYourself
from .models import Profile
from .pagination import ProfilePagination
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer
from .serializers import UpdateProfileSerializer, ProfileSerializer, FollowingSerializer

User = get_user_model()


class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = ProfilePagination
    renderer_classes = (ProfilesJSONRenderer,)


class ProfileDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    renderer_classes = (ProfileJSONRenderer,)

    def get_queryset(self):
        queryset = Profile.objects.select_related("user")
        return queryset

    def get_object(self):
        user = self.request.user
        profile = self.get_queryset().get(user=user)
        return profile


class UpdateProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateProfileSerializer
    parser_classes = [MultiPartParser]
    renderer_classes = (ProfileJSONRenderer,)

    def get_object(self):
        profile = self.request.user.profile
        return profile

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            profile = Profile.objects.get(user__id=request.user.id)
            follower_profiles = profile.followers.all()
            serializer = FollowingSerializer(follower_profiles, many=True)
            context = {
                "status_code": status.HTTP_200_OK,
                "followers_count": follower_profiles.count(),
                "followers": serializer.data,
            }
            return Response(context, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FollowingListView(APIView):
    def get(self, request, user_id, format=None):
        try:
            profile = Profile.objects.get(user__id=request.user_id)
            following_profiles = profile.following.all()
            users = [profile.user for profile in following_profiles]
            serializer = FollowingSerializer(users, many=True)
            context = {
                "status_code": status.HTTP_200_OK,
                "followings_count": following_profiles.count(),
                "users_i_follow": serializer.data,
            }
            return Response(context, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FollowView(APIView):
    def post(self, request, user_id, format=None):
        try:
            # get my profile
            follower = Profile.objects.get(user=self.request.user)
            user_profile = request.user.profile

            # get the profile of the user i want to follow
            profile = Profile.objects.get(user__id=user_id)

            if profile == follower:
                raise CantFollowYourself()

            if user_profile.check_following(profile):
                context = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": f"You are already following {profile.user.get_full_name}",
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            user_profile.follow(profile)
            send_mail(
                subject="A new user follows you",
                message=f"Hi {profile.user.get_short_name}!!, the user {user_profile.user.get_full_name} follows you",
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[profile.user.email],
                fail_silently=True,
            )
            context = {
                "status_code": status.HTTP_200_OK,
                "message": f"You are now following {profile.user.get_full_name}",
            }
            return Response(context, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            raise NotFound("You can't follow a profile that does not exist")


class UnFollowView(APIView):
    def post(self, request, user_id, format=None):
        try:
            # get my profile
            follower = Profile.objects.get(user=self.request.user)
            user_profile = request.user.profile

            # get the profile of the user i want to unfollow
            profile = Profile.objects.get(user__id=user_id)

            if profile == follower:
                raise CantFollowYourself()

            if not user_profile.check_following(profile):
                context = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": f"You are not following {profile.user.get_full_name}",
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            user_profile.unfollow(profile)
            context = {
                "status_code": status.HTTP_200_OK,
                "message": f"You are have unfollowed {profile.user.get_full_name}",
            }
            return Response(context, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            raise NotFound("You can't follow a profile that does not exist")
