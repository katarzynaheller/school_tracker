from rest_framework import (
    mixins, 
    viewsets
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from school_tracker.accounts.models import CustomUser
from school_tracker.accounts.serializers import (
    PasswordUpdateSerializer,
    UserUpdateSerializer,
    UserSerializer    
)


class UserViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    This endpoint is used as personal data update in user profile
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    serializer_map = {
        "update_user": UserUpdateSerializer,
        "change_password": PasswordUpdateSerializer
    }

    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_map.get(self.action, self.serializer_class)
    
    def get_queryset(self):
        from school_tracker.accounts.models import CustomUser
        return CustomUser.objects.filter(id=self.request.user.id).annotate_full_name()

    def get_object(self):
        return self.get_queryset().filter(id=self.request.user.id).first()

    def list(self, request, *args, **kwargs):
        return mixins.RetrieveModelMixin.retrieve(self, request, *args, **kwargs)

    @action(methods=["put", "patch"], url_path="profile", detail=False)
    def update_user(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["post"], url_path="password", detail=False)
    def change_password(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)