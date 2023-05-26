from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import (
    ParentOnlyViewAndTeacherEdit,
    OnlyStaffCanSeeListViews,
    GroupDetailViewForRelatedTeacher
)
from .models import Child, Parent, Group
from .serializers import ChildSerializer, ParentSerializer, GroupSerializer


class ChildListView(generics.ListCreateAPIView):
    permission_classes = [OnlyStaffCanSeeListViews]
    queryset = Child.objects.all()
    serializer_class = ChildSerializer


class ChildDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [ParentOnlyViewAndTeacherEdit]
    serializer_class = ChildSerializer

    def get_object(self):
        try: 
            obj = Child.objects.get(pk=self.kwargs['pk'])
            self.check_object_permissions(self.request, obj)
            return obj
        except ObjectDoesNotExist:
            raise Http404 


class ParentListView(generics.ListCreateAPIView):
    permission_classes = [OnlyStaffCanSeeListViews]
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer


class ParentDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ParentSerializer

    def get_object(self):
        try: 
            obj = Parent.objects.get(pk=self.kwargs['pk'])
            self.check_object_permissions(self.request, obj)
            return obj
        except ObjectDoesNotExist:
            return False

class GroupDetailView(generics.RetrieveAPIView):
    permission_classes = [GroupDetailViewForRelatedTeacher]
    serializer_class = GroupSerializer

    def get_object(self):
        obj = Group.objects.get(pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

class GroupListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

