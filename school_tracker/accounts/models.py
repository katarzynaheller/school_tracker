from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


from school_tracker.accounts.managers import CustomUserManager
from school_tracker.accounts.enums import UserTypeEnum


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

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    #override model's save() method to automatically set is_staff for Teacher instances
    def save(self, *args, **kwargs):
        if self.is_superuser or self.user_type == self.TEACHER :
            self.is_staff = True 
        else:
            self.user_type = self.PARENT
            self.is_staff = False

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
