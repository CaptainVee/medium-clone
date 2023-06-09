from django import forms
from django.contrib.auth import forms as admin_form
from django.contrib.auth import get_user_model

User = get_user_model()


class UserChangeForm(admin_form.UserChangeForm):
    class Meta(admin_form.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_form.UserCreationForm):
    class Meta(admin_form.UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "email")

    error_messages = {
        "duplicate_email": "A User with this email already exist",
    }

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])
