from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    fullname = serializers.SerializerMethodField(read_only=True)
    profile_photo = serializers.SerializerMethodField()
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "email",
            "fullname",
            "profile_photo",
            "country",
            "gender",
            "phone_number",
            "city",
            "tiwtter_handle",
            "about_me",
        ]

    def get_full_name(self, obj):
        first_name = obj.user.first_name.title()
        last_name = obj.user.last_name.title()
        return f"{first_name} {last_name}"

    def get_profile_photo(self, obj):
        return obj.profile_photo.url


class UpdateProfileSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "profile_photo",
            "country",
            "gender",
            "phone_number",
            "city",
            "tiwtter_handle",
            "about_me",
        ]


class FollowingSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    model = Profile
    fields = [
        "first_name",
        "last_name",
        "profile_photo",
        "tiwtter_handle",
        "about_me",
    ]
