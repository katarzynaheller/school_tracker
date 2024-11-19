from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from school_tracker.members.models import (
    AssignedTeacher,
    Child, 
    Group,
    Parent,
    Teacher
)
from school_tracker.members.serializers import (
    ChildSerializer, 
    GroupSerializer
)
from school_tracker.utils.enums import (
    UserTypeEnum, 
    AssignedTeacherTypeEnum
)

CustomUser = get_user_model()


class MembersTests(TestCase):
    def setUp(self):
        self.userparent = CustomUser.objects.create_user(
            email= 'testuser@mail.com',
            first_name = 'Test',
            last_name = "User",
            password = 'secret1234',
            user_type = UserTypeEnum.parent
        )

        self.userteacher = CustomUser.objects.create_user(
            email= 'testteacher@mail.com',
            first_name = 'Test',
            last_name = "User",
            password = 'secret1234',
            user_type = UserTypeEnum.teacher
        )

        self.group = Group.objects.create(
            group_name = "Ants"
        )
        self.teacher = Teacher.objects.create(user = self.userteacher)

        self.parent = Parent.objects.create(user=self.userparent)
        self.child = Child.objects.create(
            first_name = 'Test',
            last_name = "Child",
            birth_date = date(2022,3,6),
            group = self.group,
        )
        self.child.parents.add(self.parent)

    def test_parent_model(self):
        self.assertEqual(str(self.parent), "testuser@mail.com")

    def test_child_model(self):
        self.assertEqual(self.child.age, 2)
        self.assertNotEqual(self.child.age, 7)
        self.assertEqual(str(self.child), 'Test Child')
        self.assertIn(self.child, self.parent.children.all())

    def test_teacher_model(self):
        self.assertEqual(str(self.teacher), "testteacher@mail.com")

    def test_group_model(self):
        self.assertEqual(str(self.group), "Ants")
        self.assertEqual(self.group.group_students.count(), 1)
        self.assertIn(self.child, self.group.group_students.all())


class MembersDetailViewTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email= 'testuser@mail.com',
            first_name = 'Test',
            last_name = "User",
            password = 'secret1234',
            user_type = UserTypeEnum.parent
        )
    
        self.parent = Parent.objects.create(user=self.user)
        self.group = Group.objects.create(
            group_name = "Ia"
        )
        
        self.child = Child.objects.create(
            first_name = 'Test Child',
            last_name = 'Abc',
            birth_date = date(2022,3,6),
            group = self.group,
        )
        self.child.parents.add(self.parent)
        
    def test_models(self):
        self.assertEqual(str(self.parent), "testuser@mail.com")
        self.assertIn(self.child, self.parent.children.all())

    def test_parent_detail(self):
        url = reverse("me-detail", kwargs={'pk':self.user.pk})
        self.client.force_authenticate(user=self.parent.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_child_detail(self):
        url = reverse("children-detail", kwargs={"child_id": self.child.id})
        self.client.force_authenticate(user=self.parent.user)
        response = self.client.get(url)
        self.assertIn(self.child, self.parent.children.all())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_parent_cannot_access_list_children(self):
        url = reverse("children-list")
        self.client.force_authenticate(user=self.parent.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class MembersListViewTests(APITestCase):
    
    def setUp(self):
        self.related_user_teacher= CustomUser.objects.create_user(
            email= 'testteacher@mail.com',
            first_name = 'Test',
            last_name = "Teacher",
            password = 'secret1234',
            is_staff = True,
            user_type = UserTypeEnum.teacher
        )

        self.user_parent = CustomUser.objects.create_user(
            email= 'testparent@mail.com',
            first_name = 'Test',
            last_name = "Parent",
            password = 'secret1234',
            user_type = UserTypeEnum.parent
        )

        self.unrelated_user_teacher = CustomUser.objects.create_user(
            email= 'differentteacher@mail.com',
            first_name = 'Different',
            last_name = "Teacher",
            password = 'secret1234',
            is_staff = True,
            user_type = UserTypeEnum.teacher
        )
        
        self.teacher = Teacher.objects.create(user=self.related_user_teacher)
        self.group = Group.objects.create(
            group_name = "Ants"
        )
        self.assigned_teacher = AssignedTeacher.objects.create(
            teacher = self.teacher,
            group = self.group,
            assigned_type = AssignedTeacherTypeEnum.primary
        )
        self.unrelated_teacher = Teacher.objects.create(user=self.unrelated_user_teacher)

        self.parent = Parent.objects.create(user=self.user_parent)

        self.child_one = Child.objects.create(
            first_name = 'Test',
            last_name = "Child",
            birth_date = date(2022,3,6),
            group = self.group
        )
        self.child_one.parents.add(self.parent)

        self.child_two = Child.objects.create(
            first_name = 'Test1',
            last_name = "Child1",
            birth_date = date(2022,3,6),
            group = self.group
        )
        self.child_two.parents.add(self.parent)
        
        self.url = reverse('children-list')

    def test_models(self):
        self.assertEqual(self.related_user_teacher.email, self.teacher.user.email)
        self.assertIn(self.child_one, self.parent.children.all())
        self.assertIn(self.child_two, self.parent.children.all())
        self.assertTrue(self.group.assigned_teachers.filter(teacher=self.teacher).exists())

    def test_related_teacher_can_read_list_children(self): 
        self.client.force_authenticate(user=self.related_user_teacher)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_related_parent_can_read_list_children(self): 
        self.client.force_authenticate(user=self.user_parent)
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_group_detail_view_for_related_teacher(self):

        self.client.force_authenticate(user=self.related_user_teacher)
        url = reverse('groups-detail', kwargs={"group_id": self.group.id})
       
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unrelated_teacher_can_read_list_children(self):
        self.client.force_authenticate(user=self.unrelated_user_teacher)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_group_detail_not_for_unrelated_teacher(self):
        self.client.force_authenticate(user = self.unrelated_user_teacher)
        
        url = reverse('groups-detail', kwargs={"group_id": self.group.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
