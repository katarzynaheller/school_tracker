from rest_framework import (
    mixins,
    viewsets, 
    status
)
from rest_framework.response import Response

from school_tracker.members.permissions import TeacherOrParentRelatedToChildPermission
from school_tracker.schedules.models import DayPlan
from school_tracker.schedules.serializers import (
    DayPlanCreateUpdateSerializer,
    DayPlanSerializer
)
from school_tracker.utils.dicttools import get_values_from_dict


class DayPlanViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [TeacherOrParentRelatedToChildPermission]
    serializer_class = DayPlanSerializer
    lookup_field = "child_id"

    serializer_map = {
        "create": DayPlanCreateUpdateSerializer,
        "partial_update": DayPlanCreateUpdateSerializer
    }

    _dayplan_creation_keys = ["meals_at_school", "behaviour", "summary"]


    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.action, self.serializer_class)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['date'] = self.kwargs.get('date')
        return context

    def get_queryset(self):
        child_id = self.kwargs.get("child_id")
        return DayPlan.objects.fetch_by_child_id(child_id)

    def retrieve(self, request, *args, **kwargs):
        date = kwargs.get('date')
        child_id = self.kwargs.get("child_id")
        try:
            instance = DayPlan.objects.fetch_by_child_and_date(child_id, date)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except DayPlan.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer):
        data = get_values_from_dict(serializer.validated_data, self._dayplan_creation_keys)
        data["child"] = self.kwargs.get("child_id")
        serializer.save()
