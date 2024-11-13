from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from school_tracker.members.models import (
    Child, 
    Group,
    Parent,
    Teacher
)
from school_tracker.members.serializers import (
    ChildSerializer, 
    GroupSerializer
)
from school_tracker.utils.enums import UserTypeEnum

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
    '''
    Because of permissions - child detail view is available for child's parent
    '''
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email= 'testuser@mail.com',
            first_name = 'Test',
            last_name = "User",
            password = 'secret1234',
            user_type = CustomUser.PARENT
        )
    
        self.client.force_authenticate(user = self.user)
        self.parent = Parent.objects.create(user = self.user)
        
        self.child = Child.objects.create(
            full_name = 'Test Child',
            birth_date = date(2022,3,6),
            parent = self.parent
        )
        
    
    def test_can_read_parent_detail(self):
        response = self.client.get(reverse('parent_detail', args=[self.parent.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_read_child_detail(self):
        response = self.client.get(reverse('child_detail', args=[self.child.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_parent_cannot_access_list_children(self):
        response = self.client.get(reverse('children_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class MembersListViewTests(APITestCase):
    '''
    Child list view is available only for members with is_staff status
    '''
    
    def setUp(self):
        self.userteacher= CustomUser.objects.create_user(
            email= 'testteacher@mail.com',
            first_name = 'Test',
            last_name = "Teacher",
            password = 'secret1234',
            is_staff = True,
            user_type = UserTypeEnum.teacher
        )

        self.userparent = CustomUser.objects.create_user(
            email= 'testparent@mail.com',
            first_name = 'Test',
            last_name = "Parent",
            password = 'secret1234',
            user_type = UserTypeEnum.parent
        )

        self.unrelatedteacher = CustomUser.objects.create_user(
            email= 'differentteacher@mail.com',
            first_name = 'Different',
            last_name = "Teacher",
            password = 'secret1234',
            is_staff = True,
            user_type = UserTypeEnum.teacher
        )
        
        self.teacher = Teacher.objects.create(user = self.userteacher)
        self.parent = Parent.objects.create(user = self.userparent)
        self.teacher1 = Teacher.objects.create(user = self.unrelatedteacher)
        self.group = Group.objects.create(
            group_name = "Ants"
        )
        self.child = Child.objects.create(
            first_name = 'Test',
            last_name = "Child",
            birth_date = date(2022,3,6),
            group = self.group
        )
        self.child.parents.add(self.parent)

        self.child = Child.objects.create(
            first_name = 'Test1',
            last_name = "Child1",
            birth_date = date(2022,3,6),
            group = self.group
        )
        self.child.parents.add(self.parent)
        

        self.url = reverse('children_list')

    def test_teacher_can_read_list_children(self):
        # when
        self.client.force_authenticate(user = self.userteacher)
        response = self.client.get(self.url)

        # then
        child = Child.objects.all()
        serializer = ChildSerializer(child, many = True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_parent_cannot_read_list_children(self):
        #authenticate as a parent user
        self.client.force_authenticate(user = self.userparent)

        #make a GET request to the tested URL
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_group_detail_view_for_related_teacher(self):
        #authenticate as a teacher user
        self.client.force_authenticate(user = self.userteacher)

        #make a GET request to the teacher's group's detail URL
        response = self.client.get(reverse('group_detail', args = [self.group.pk]))

        #retrieve data to compare with response
        group_serializer = GroupSerializer(instance=self.group)
        
        self.assertEqual(response.data, group_serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_group_detail_not_for_unrelated_teacher(self):
        #authenticate as a unrelated teacher user
        self.client.force_authenticate(user = self.unrelatedteacher)
        
        #make a GET request to the teacher's group's detail URL
        response = self.client.get(reverse('group_detail', args = [self.group.pk]))
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
