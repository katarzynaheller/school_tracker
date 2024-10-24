from django.db.models import Manager

from school_tracker.accounts.models import CustomUser
from school_tracker.members.models import (
    Child,
    Group,
    Teacher
)
from school_tracker.utils.enums import UserTypeEnum

class ParentManager(Manager):
    def create_with_child(self, member_data, child_data):
        if not child_data:
            raise ValueError("Parent must be assigned with at least one child.")
        
        child, created = Child.objects.get_or_create(**child_data)

        member = CustomUser.objects.create_user(
            email=member_data['email'],
            first_name=member_data["first_name"],
            last_name=member_data["last_name"],
            password=None,
            user_type=UserTypeEnum.parent,
        )

        parent = self.create(user=member, child=child)
        return parent


class AssignedTeacherManager(Manager):
    def create_with_group_assign(self, member_data, group_data):
        member = CustomUser.objects.create_user(
            email=member_data["email"],
            first_name=member_data["first_name"],
            last_name=member_data["last_name"],
            password=None,
            user_type=UserTypeEnum.teacher,
        )
        teacher = Teacher.objects.create(user=member)
        
        group = Group.object.create(**group_data)

        assigned_teacher = self.create(
            teacher=teacher,
            group=group,
            assigned_type= member_data.pop('assigned_type')
            **member_data
        )

        return assigned_teacher, group

        
