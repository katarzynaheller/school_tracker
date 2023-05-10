from django.http import Http404
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import (
    ParentOnlyViewAndTeacherEdit,
    OnlyStaffCanSeeListViews,
)
from .models import Child, Parent, Group
from .serializers import ChildSerializer, ParentSerializer, GroupSerializer


class ChildListView(generics.ListCreateAPIView):
    permission_classes = [OnlyStaffCanSeeListViews]
    queryset = Child.objects.all()
    serializer_class = ChildSerializer


class ChildDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [ParentOnlyViewAndTeacherEdit]
    queryset = Child.objects.all()
    serializer_class = ChildSerializer


class ParentListView(generics.ListCreateAPIView):
    permission_classes = [OnlyStaffCanSeeListViews]
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer


class ParentDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

class GroupDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

