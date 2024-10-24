from rest_framework import (
    mixins, 
    viewsets
)
from school_tracker.accounts.models import CustomUser
from school_tracker.accounts.serializers import (
    UserCreateUpdateSerializer,
    UserSerializer    
)
from school_tracker.utils.permissions import IsAdminUser
from school_tracker.utils.dicttools import get_values_from_dict

class UserViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    serializer_map = {
        "create": UserCreateUpdateSerializer,
        "update": UserCreateUpdateSerializer,
        "partial_update": UserCreateUpdateSerializer
    }

    _user_creation_keys = ["email", "first_name", "last_name", "user_type"]


    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.action, self.serializer_class)

    def perform_create(self, serializer):
        data = get_values_from_dict(serializer.validated_data, self._user_creation_keys)
        user = CustomUser.objects.create(**data)