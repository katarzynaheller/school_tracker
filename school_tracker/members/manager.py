from django.db.models import Manager

from school_tracker.accounts.models import CustomUser
from school_tracker.utils.enums import UserTypeEnum


class ParentManager(Manager):
    def create_with_invitation(self, parent):
        """
        Method for sending email invitation to app with link to set password
        """
        pass


class ChildManager(Manager):
    def create_with_parent(self, parent_data, child_data):
        from school_tracker.members.models import Group, Parent

        if not parent_data:
            raise ValueError("Child must be assigned with at least one parent.")
        
        group = Group.objects.get(id=child_data["group_id"])
        member = CustomUser.objects.create_user(
            email=parent_data['email'],
            first_name=parent_data["first_name"],
            last_name=parent_data["last_name"],
            password=None,
            user_type=UserTypeEnum.parent,
        )
        parent = Parent.objects.create(user=member)
        # Send invitation for Parent user to app
        Parent.objects.create_with_send_invitation(parent)

        child, created = self.get_or_create(
            first_name=child_data["first_name"],
            last_name=child_data["last_name"],
            birth_date=child_data["birth_date"],
            group = group,
        )
        child.parents.add(parent)
        return child


class AssignedTeacherManager(Manager):
    def create_with_group_assign(self, teacher_data, group_data):
        from school_tracker.members.models import Group, Teacher
        member = CustomUser.objects.create_user(
            email=teacher_data["email"],
            first_name=teacher_data["first_name"],
            last_name=teacher_data["last_name"],
            password=None,
            user_type=UserTypeEnum.teacher,
        )
        teacher = Teacher.objects.create(user=member)
        
        group, created = Group.object.get_or_create(
            id=group_data.get("id"),
            group_name=group_data.get("group_name")
        )

        assigned_teacher = self.create(
            teacher=teacher,
            group=group,
            assigned_type=teacher_data.pop('assigned_type')
            **teacher_data
        )
        return assigned_teacher
    
class GroupManager(Manager):
    def with_related_teachers(self, group_id):
        return self.get_queryset().filter(id=group_id).prefetch_related(
            "assigned_teachers__user"
        ).values_list("assigned_teachers__teacher__user__first_name", flat=True)

    def with_related_children(self, group_id):
        return self.get_queryset().filter(id=group_id).prefetch_related(
            "group_students"
        ).values_list("group_students__first_name", flat=True)

    def with_related_parents(self, group_id):
        return self.get_queryset().filter(id=group_id).prefetch_related(
            "group_students__parents__user"
        ).values_list("group_students__parents__user__first_name", flat=True).distinct()