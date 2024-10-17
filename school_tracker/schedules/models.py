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
    FULL = "FL"
    HALF = "HF"
    FEW = "FW"
    NOTMARKED = "NM"
    FOOD_CHOICES = [
        (FULL, "Fully eaten"),
        (HALF, "Halfy eaten"),
        (FEW, "Poorly eaten"),
        (NOTMARKED, "Not marked"),
    ]
    meals_at_school = models.CharField(
        max_length=2, choices=FOOD_CHOICES, default=NOTMARKED
    )
    EVERYTHING_OK = "OK"
    NEED_TALK = "NT"
    NOTDEFINED = "ND"

    BEHAVIOUR_CHOICES = [
        (EVERYTHING_OK, "Everything ok"),
        (NEED_TALK, "We need to talk"),
        (NOTDEFINED, "Not defined"),
    ]
    behaviour = models.CharField(
        max_length=2, choices=BEHAVIOUR_CHOICES, default=NOTDEFINED
    )
    summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.child.full_name
