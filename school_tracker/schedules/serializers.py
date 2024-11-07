from rest_framework import serializers

from school_tracker.schedules.models import (
    DayPlan,
    Event
)
from school_tracker.utils.serializers import ReadOnlyModelSerializer

class DayPlanSerializer(ReadOnlyModelSerializer):
    events = serializers.SerializerMethodField()

    class Meta:
        model = DayPlan
        fields = (
            "day",
            "child",
            "meals_at_school",
            "behaviour",
            "summary",
            "events",
        )
        read_only_fields = fields

    def get_events(self):
        events = Event.objects.filter(date=self.instance.day)
        return [event.title for event in events]


class DayPlanCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayPlan
        fields = (
            "day",
            "child",
            "meals_at_school",
            "behaviour",
            "summary",
        )
        read_only_fields = (
            "day",
            "child",
        )

    def validate_day(self, value):
        if value < self.instance.date.today():
            raise serializers.ValidationError("The date cannot be in the past.")
        return value
