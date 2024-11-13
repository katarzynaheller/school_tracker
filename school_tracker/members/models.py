from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from school_tracker.utils.enums import (
    AssignedTeacherTypeEnum,
    UserTypeEnum
)

CustomUser = get_user_model()

class Teacher(models.Model):
    user =  models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.email
    
    def save(self, *args, **kwargs):
        if self.user.user_type != UserTypeEnum.teacher:
            raise ValidationError("Teacher must have user_type set to 'teacher'.")
        super().save(*args, **kwargs)

class Parent(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
    
    def save(self, *args, **kwargs):
        if self.user.user_type != UserTypeEnum.parent:
            raise ValidationError("Parent must have user_type set to 'parent'.")
        super().save(*args, **kwargs)

class Group(models.Model):
    group_name = models.CharField(max_length=50)

    def __str__(self):
        return self.group_name


class AssignedTeacher(models.Model):
    teacher =  models.ForeignKey(Teacher, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="assigned_teachers")
    assigned_type = models.CharField(
        max_length=20, choices=AssignedTeacherTypeEnum.choices, default = AssignedTeacherTypeEnum.primary
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return f"{self.teacher.user.email} - {self.group.group_name}"


class Child(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_students")
    parents = models.ManyToManyField(Parent, related_name="children")
    
    @property
    def age(self):
        today = timezone.now().date()
        age = int(
            today.year
            - (self.birth_date.year)
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )
        return age

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = "Child"
        verbose_name_plural = "Children"