from rest_framework import permissions
from django.shortcuts import get_object_or_404

from school_tracker.utils.enums import UserTypeEnum

class MessagePermission(permissions.BasePermission):
    message = "Only message sender/receiver can see this content."
        
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        
        if request.user.id == obj.sender.id:
            return True
        
        elif request.user.user_type == UserTypeEnum.parent:
            return obj.child.parents.filter(user__id=request.user.id).exists()
        
        elif request.user.user_type == UserTypeEnum.teacher:
            return obj.child.group.assigned_teachers.filter(teacher__user__id=request.user.id).exists()