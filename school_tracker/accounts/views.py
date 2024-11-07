from rest_framework import (
    mixins, 
    viewsets
)
from rest_framework.permissions import IsAdminUser

from school_tracker.accounts.models import CustomUser
from school_tracker.accounts.serializers import (
    UserUpdateSerializer,
    UserSerializer    
)
from school_tracker.utils.dicttools import get_values_from_dict

class UserViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    This endpoint is used as personal data update in user profile
    """
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    serializer_map = {
        "update": UserUpdateSerializer,
        "partial_update": UserUpdateSerializer
    }

    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.action, self.serializer_class)