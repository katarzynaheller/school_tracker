from enum import auto

from django.db import models


class UserTypeEnum(models.TextChoices):
    """
    Types for user profile in app
    """
    teacher = auto()
    parent = auto()
    manager = auto()
    admin = auto()
    unset = auto()