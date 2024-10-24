from rest_framework import serializers

from school_tracker.schedules.models import DayPlan
from school_tracker.utils.serializers import ReadOnlyModelSerializer

class DayPlanSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = DayPlan
        fields = (
            "day",
            "child",
            "meals_at_school",
            "behaviour",
            "summary",
            "event",
        )
        read_only_fields = fields

class DayPlanCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayPlan
        fields = (
            "day",
            "child",
            "meals_at_school",
            "behaviour",
            "summary",
            "event",
        )
        read_only_fields = (
            "day",
            "child",
            "event"
        )

    def validate_day(self, value):
        if value < date.today():
            raise serializers.ValidationError("The date cannot be in the past.")
        return value
