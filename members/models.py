from django.db import models
from accounts.models import CustomUser
from django.utils import timezone


class Parent(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class Child(models.Model):
    full_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name="child")
    
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
    def group_member(self):
        groups = self.group_set.all()
        return ", ".join([group.group_name for group in groups])

    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = "Child"
        verbose_name_plural = "Children"

class Teacher(models.Model):
    user =  models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email


class Group(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    members = models.ManyToManyField(Child)
    group_name = models.CharField(max_length=50)

    def __str__(self):
        return self.group_name

