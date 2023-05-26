from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from datetime import date

from accounts.models import CustomUser
from .models import Child, Parent,Teacher,Group
from .serializers import ChildSerializer, ParentSerializer, GroupSerializer

class MembersTests(TestCase):
    def setUp(self):
        self.userparent = CustomUser.objects.create_user(
            email= 'testuser@mail.com',
            first_name = 'Test',
            last_name = "User",
            password = 'secret1234',
            user_type = CustomUser.PARENT
        )

        self.userteacher = CustomUser.objects.create_user(
            email= 'testteacher@mail.com',
            first_name = 'Test',
            last_name = "User",
            password = 'secret1234',
            user_type = CustomUser.TEACHER
        )
        self.parent = Parent.objects.create(user=self.userparent)
        self.child = Child.objects.create(
            full_name = 'Test Child',
            birth_date = date(2022,3,6),
            parent = self.parent
        )
        self.teacher = Teacher.objects.create(user = self.userteacher)
        self.group = Group.objects.create(
            teacher = self.teacher,
            group_name = "Ants"
        )

        self.group.members.add(self.child)


    def test_parent_model(self):
        self.assertEqual(str(self.parent), "testuser@mail.com")

    def test_child_model(self):
        self.assertEqual(self.child.age, 1)
        self.assertNotEqual(self.child.age, 7)
        self.assertEqual(str(self.child), 'Test Child')
        self.assertIn(self.child, self.parent.child.all())

    def test_teacher_model(self):
        self.assertEqual(str(self.teacher), "testteacher@mail.com")

    def test_group_model(self):
        self.assertEqual(str(self.group), "Ants")
        self.assertEqual(self.group.members.count(), 1)
        self.assertIn(self.child, self.group.members.all())

   


User = get_user_model()

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
            user_type = CustomUser.TEACHER
        )

        self.userparent = CustomUser.objects.create_user(
            email= 'testparent@mail.com',
            first_name = 'Test',
            last_name = "Parent",
            password = 'secret1234',
            user_type = CustomUser.PARENT
        )

        self.unrelatedteacher = CustomUser.objects.create_user(
            email= 'differentteacher@mail.com',
            first_name = 'Different',
            last_name = "Teacher",
            password = 'secret1234',
            is_staff = True,
            user_type = CustomUser.TEACHER
        )
        
        self.teacher = Teacher.objects.create(user = self.userteacher)
        self.parent = Parent.objects.create(user = self.userparent)
        self.teacher1 = Teacher.objects.create(user = self.unrelatedteacher)
        
        self.child = Child.objects.create(
            full_name = 'Test Child',
            birth_date = date(2022,3,6),
            parent = self.parent
        )

        self.child1 = Child.objects.create(
            full_name = 'One Child',
            birth_date = date(2022,3,6),
            parent = self.parent
        )
        self.group = Group.objects.create(
            teacher = self.teacher,
            group_name = "Ants"
        )

        self.group.members.add(self.child)
        self.url = reverse('children_list')

    def test_teacher_can_read_list_children(self):
        #authenticate as a teacher user
        self.client.force_authenticate(user = self.userteacher)

        #make a GET request to the tested URL
        response = self.client.get(self.url)

        #compare the response data from the API with the expected serialized data.
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
