from django.db import models
from django.utils import timezone

from school_tracker.members.models import Child
from school_tracker.utils.enums import (
    BehaviourStatusEnum,
    MealStatusEnum
)
from school_tracker.schedules.manager import DayPlanManager


class Event(models.Model):
    """
    Model to store special events planned in a given institution or group
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.title


class DayPlan(models.Model):
    """
    Model to represent daily activity and status
    """
    day = models.DateField(auto_now=True)
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name="dayplans")
    meals_at_school = models.CharField(
        max_length=20, choices=MealStatusEnum.choices, default=MealStatusEnum.not_specified
    )
    behaviour = models.CharField(
        max_length=20, choices=BehaviourStatusEnum.choices, default=BehaviourStatusEnum.not_specified
    )
    summary = models.TextField(null=True, blank=True)

    objects = DayPlanManager()

    def __str__(self):
        return f"Dayplan for {self.child.full_name} at {self.day}"

    @property
    def events(self):
        if events := Event.objects.filter(date=self.day):
            return [event.title for event in events] if events.exists() else "No events for today."
