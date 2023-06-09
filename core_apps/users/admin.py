from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    odering = ["email"]
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    list_display = "__all__"
    list_display_links = ["pkid", "id", "email"]
    list_filter = ["email", "is_staff", "is_active"]
    fieldsets = (
        (_("Login Credentials"), {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        None,
        {
            "classes": ("wide",),
            "fields": ("first_name", "last_name", "email", "password1", "password2"),
        },
    )
    search_fields = ["first_name", "last_name", "email", "password1", "password2"]


admin.site.register(User, UserAdmin)
