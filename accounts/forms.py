from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("email", "first_name", "last_name", "user_type")


class CustomUserChangeForm(UserChangeForm):
    model = CustomUser
    fields = ("email", "first_name", "last_name", "user_type")
