from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Custom manager to overwrite authentication required credentials
    (email instead of username)"""

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("Email required"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff set to True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser set to True"))

        return self.create_user(email, password, **extra_fields)

    def all_members_inside_institution(self, institution_id: int):
            """
            Return all users inside institution
            """
            return CustomUser.objects.filter(institution__id=institution_id)

    def fetch_all_teachers_inside_instutution(self, user_type, institution_id: int):
        """
        Return all teachers inside institution
        """
        return CustomUser.objects.filter(
            user_type=UserTypeEnum.teacher,
            institution__id=institution_id
        )

    def fetch_all_parents_for_group_students(self, group_id: int):
        """
        Return all parents inside group students
        """
        return CustomUser.objects.filter(
            parent__child__group__id=group_id
        ).distinct()