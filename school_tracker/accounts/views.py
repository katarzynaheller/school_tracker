from django.shortcuts import get_object_or_404
from rest_framework import (
    mixins, 
    viewsets,
    status
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from school_tracker.accounts.models import CustomUser
from school_tracker.accounts.serializers import (
    PasswordUpdateSerializer,
    MeUpdateSerializer,
    UserUpdateSerializer,
    UserSerializer    
)
from school_tracker.members.permissions import IsOwner


class UserViewSet(mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    This endpoint is used for user data management (for admins)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    serializer_map = {
        "update": UserUpdateSerializer,
    }

    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.action, self.serializer_class)
    
    
class MeViewSet(mixins.UpdateModelMixin, 
                mixins.RetrieveModelMixin,
                viewsets.GenericViewSet):
    """
    This endpoint is used for user data management (for users)
    """
    permission_classes = [IsOwner]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    serializer_map = {
        "update": MeUpdateSerializer,
        "partial_update": MeUpdateSerializer,
        "change_password": PasswordUpdateSerializer
    }

    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.action, self.serializer_class)
    
    @action(methods=["post"], url_path="password", detail=False)
    def change_password(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)