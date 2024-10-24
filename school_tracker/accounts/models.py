from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


from school_tracker.accounts.manager import CustomUserManager
from school_tracker.utils.enums import UserTypeEnum


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email"), unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_type = models.CharField(
        max_length=20, choices=UserTypeEnum.choices, default=UserTypeEnum.unset
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]

    objects = CustomUserManager()

    def __init__(self, *args, **kwargs):
        super(CustomUser, self).__init__(*args, **kwargs)
        self._initial_email = self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    @staticmethod
    def get_admin_users():
        return CustomUser.objects.filter(user_type=UserTypeEnum.admin)
    
    def _get_username(self):
        if self._state.adding and not self.pk:
            return self.username or self.email
        if self._initial_email != self.email and self.email is not None:
            return self.email
        return self.username

    def save(self, *args, **kwargs):
        '''
        Assign staff status to teacher, 
        check for existing email 
        and assign email as username
        '''
        if self.is_superuser or self.user_type == UserTypeEnum.teacher:
            self.is_staff = True 
        elif self.user_type == UserTypeEnum.parent:
            self.is_staff = False

        if self.email:
            if CustomUser.objects.filter(
                email=self.email
            ).exclude(
                pk=self.pk
            ).exists():
                raise Exception("User with this email address already exists.")
        
        self.username = self._get_username()
        return super().save(*args, **kwargs)

    