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

class AssignedTeacherTypeEnum(models.TextChoices):
    """
    Types of assigment for a teacher
    """
    primary = auto()
    support = auto()


class BehaviourStatusEnum(models.TextChoices):
    """
    Quick status for student's behaviour
    """
    great_day = auto()
    ok_day = auto()
    might_be_better = auto()
    talk_needed = auto()
    not_specified = auto()


class MealStatusEnum(models.TextChoices):
    """
    Quick status about meals
    """
    full = auto()
    half = auto()
    little = auto()
    not_specified = auto()
    important_note = auto()


