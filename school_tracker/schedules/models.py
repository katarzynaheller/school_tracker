from django.db import models
from django.utils import timezone

from school_tracker.members.models import Child


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.title


class DayPlan(models.Model):
    day = models.DateField(auto_now=True)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    meals_at_school = models.CharField(
        max_length=20, choices=MealStatusEnum.choices, default=MealStatusEnum.not_specified
    )
    behaviour = models.CharField(
        max_length=20, choices=BehaviourStatusEnum.choices, default=BehaviourStatusEnum.not_specified
    )
    summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.child.full_name
