from rest_framework import serializers

from school_tracker.schedules.models import DayPlan


class DayPlanSerializer(serializers.ModelSerializer):
    class Meta():
        model = DayPlan
        fields = (
            "day",
            "child",
            "meals_at_school",
            "behaviour",
            "summary",
            "event",
        )
