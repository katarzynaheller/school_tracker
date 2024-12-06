from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from school_tracker.utils.enums import UserTypeEnum
from school_tracker.accounts.models import CustomUser
from school_tracker.chats.models import Message
from tests.factories import (
    AssignedTeacher,
    CustomUserFactory, 
    ParentFactory, 
    ChildFactory, 
    TeacherFactory, 
    GroupFactory, 
    MessageFactory
)


class TestChildViewPermissions(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.teacher = TeacherFactory()
        cls.unrelated_teacher = TeacherFactory()
        cls.group = GroupFactory()
        cls.group_one = GroupFactory()
        cls.assigned_teacher = AssignedTeacher(teacher=cls.teacher, group=cls.group)

        cls.parent = ParentFactory()
        cls.parent_another = ParentFactory()
        cls.child = ChildFactory(parents=[cls.parent], group=cls.group) 
        cls.child_another = ChildFactory(parents=[cls.parent_another], group=cls.group_one)

        cls.url = reverse('children-list')


    def test_list_child_view_for_teacher(self):
        # when:
        self.client.force_authenticate(user=self.teacher.user)
        response = self.client.get(self.url)
        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.teacher.user.is_staff, True)
        self.assertEqual(self.teacher.user.user_type, UserTypeEnum.teacher)
        self.assertEqual(len(response.data), 2)
        self.assertIn(self.child, self.group.group_students.all())

    def test_list_child_view_for_parent(self):
        # when:
        self.client.force_authenticate(user=self.parent.user)
        response = self.client.get(self.url)
        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.parent.user.is_staff, False)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(self.parent.user.user_type, UserTypeEnum.parent)
        self.assertIn(self.parent, self.child.parents.all())

    def test_parent_can_edit_related_child(self):
        # when:
        self.client.force_authenticate(user=self.parent.user)
        url = reverse("children-detail", args=[self.child.id])
        # then:
        response = self.client.patch(url, data={"name": "New Name"}, format="json")
        self.assertEqual(response.status_code, 200)

    def test_parent_cannot_delete_child(self):
        # when:
        self.client.force_authenticate(user=self.parent.user)
        url = reverse("children-detail", args=[self.child.id])
        # then:
        response = self.client.delete(url, data={"name": "New Name"}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_parent_can_edit_related_child(self):
        # when:
        self.client.force_authenticate(user=self.parent_another.user)
        url = reverse("children-detail", args=[self.child.id])
        # then:
        response = self.client.patch(url, data={"name": "New Name"}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_detail_child_view_for_unrelated_parent(self):
        # when:
        self.client.force_authenticate(user=self.parent_another.user)
        self.url = reverse("children-detail", args=[self.child.id])
        response = self.client.get(self.url)
        # then:
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_child_view_for_related_teacher(self):
        # when:
        self.client.force_authenticate(user = self.teacher.user)
        self.url = reverse('children-detail', args=[self.child.id])
        response = self.client.get(self.url)
        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.child, self.group.group_students.all())
        self.assertIn(self.teacher, [assigned_teacher.teacher for assigned_teacher in self.group.assigned_teachers.all()])

    def test_detail_view_for_unrelated_teacher(self):
        # when:
        self.client.force_authenticate(user = self.unrelated_teacher.user)
        self.url = reverse('children-detail', args=[self.child.id])
        response = self.client.get(self.url)
        # then:
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.unrelated_teacher.user.is_staff, True)
        self.assertNotIn(self.unrelated_teacher, [assigned_teacher.teacher for assigned_teacher in self.group.assigned_teachers.all()])

class TestMemberViewPermissions(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.teacher = TeacherFactory()
        cls.group = GroupFactory()

        cls.parent = ParentFactory()
        cls.child = ChildFactory(parents=[cls.parent], group=cls.group) 

        cls.url = reverse('members-list')    
    
    def test_members_view_for_teachers(self):

        # when:
        self.client.force_authenticate(self.teacher.user)
        self.url = reverse('members-list')
        response = self.client.get(self.url)

        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_members_view_for_parents(self):

        # when:
        self.client.force_authenticate(self.parent.user)
        self.url = reverse('members-list')
        response = self.client.get(self.url)

        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
      
class TestGroupViewPermissions(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.teacher = TeacherFactory()
        cls.unrelated_teacher = TeacherFactory()
        cls.group = GroupFactory()
        cls.group_one = GroupFactory()
        cls.assigned_teacher = AssignedTeacher(teacher=cls.teacher, group=cls.group)

        cls.parent = ParentFactory()
        cls.parent_another = ParentFactory()
        cls.child = ChildFactory(parents=[cls.parent], group=cls.group) 
        cls.child_another = ChildFactory(parents=[cls.parent_another], group=cls.group_one)

    def test_group_list_view_unrelated_teacher(self):
        # when:
        self.client.force_authenticate(self.unrelated_teacher.user)
        self.url = reverse('groups-list')
        response = self.client.get(self.url)
        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(self.unrelated_teacher, [assigned_teacher.teacher for assigned_teacher in self.group.assigned_teachers.all()])

    def test_group_list_view_parent(self):
        # when:
        self.client.force_authenticate(self.parent.user)
        self.url = reverse('groups-list')
        response = self.client.get(self.url)
        # then:
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_group_detail_view_related_teacher(self):
        # when:
        self.client.force_authenticate(self.teacher.user)
        self.url = reverse('groups-detail', args=[self.group.id])
        response = self.client.get(self.url)
        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.group.assigned_teachers.first().teacher, self.teacher)

    def test_group_detail_view_unrelated_teacher(self):
        # when:
        self.client.force_authenticate(self.unrelated_teacher.user)
        self.url = reverse('groups-detail', args=[self.group.id])
        # then:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(self.group.assigned_teachers.first().teacher, self.unrelated_teacher)

    def test_group_detail_view_parent(self):
        # when:
        self.client.force_authenticate(self.parent.user)
        self.url = reverse('groups-detail', args=[self.group.id])
        response = self.client.get(self.url)
        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestMeViewPermissions(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.parent = ParentFactory()
        cls.group = GroupFactory()
        cls.child = ChildFactory(parents=[cls.parent], group=cls.group)
        cls.teacher = TeacherFactory()

    def test_parent_can_access_me_profile(self):
        # when:
        self.client.force_authenticate(self.parent.user)
        self.url = reverse('me-detail', args=[self.parent.user.id])
        response = self.client.get(self.url)
        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.parent.user.email)

    def test_parent_can_update_me_profile(self):
        # when:
        self.client.force_authenticate(self.parent.user)
        self.url = reverse('me-detail', args=[self.parent.user.id])
        response = self.client.patch(self.url, data={"email": self.parent.user.email, "first_name":"New"}, format="json")
        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_teacher_can_access_me_profile(self):
        # when:
        self.client.force_authenticate(self.teacher.user)
        self.url = reverse('me-detail', args=[self.teacher.user.id])
        response = self.client.get(self.url)
        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.teacher.user.email)

    def test_teacher_can_update_me_profile(self):
        # when:
        self.client.force_authenticate(self.teacher.user)
        self.url = reverse('me-detail', args=[self.teacher.user.id])
        response = self.client.patch(self.url, data={"email": self.teacher.user.email, "first_name":"New"}, format="json")
        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_access_to_me_profile(self):
        # when:
        self.client.force_authenticate(self.teacher.user)
        self.url = reverse('me-detail', args=[self.parent.user.id])
        response = self.client.get(self.url)
        # then:
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    
class MessageViewPermissions(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.parent = ParentFactory()
        cls.group_one = GroupFactory()
        cls.group_two = GroupFactory()
        cls.child_one = ChildFactory(parents=[cls.parent], group=cls.group_one)
        cls.child_two = ChildFactory(parents=[cls.parent], group=cls.group_two)

        cls.teacher_one = TeacherFactory()
        cls.teacher_two = TeacherFactory()
        cls.teacher_unrelated = TeacherFactory()

        cls.assigned_teacher_one = AssignedTeacher(teacher=cls.teacher_one, group=cls.group_one)
        cls.assigned_teacher_two = AssignedTeacher(teacher=cls.teacher_two, group=cls.group_two)

        cls.messages_child_one = MessageFactory(sender=cls.parent.user, child=cls.child_one)
        cls.messages_child_two = MessageFactory(sender=cls.parent.user, child=cls.child_two)

    def test_list_message_view_for_teacher(self):
        # when:
        self.client.force_authenticate(self.teacher_one.user)
        self.url = reverse('messages-list')
        response = self.client.get(self.url)
        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        for message in response.data:
            self.assertIn(message["child"], self.child_one.id)
       

    def test_list_message_view_for_parent(self):
        # when:
        self.client.force_authenticate(self.parent.user)
        self.url = reverse('messages-list')
        response = self.client.get(self.url)
        #then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertContains(response, self.child_one.id)
        self.assertContains(response, self.child_two.id)
        self.assertContains(response, self.messages_child_one.id)
        self.assertContains(response, self.messages_child_two.id)
        self.assertEqual(len(response.data), 2)

    def test_detail_message_view_for_unrelated_teacher(self):
        # when:
        self.client.force_authenticate(self.teacher_unrelated.user)
        self.url = reverse('messages-detail', args=[self.child_one.id])
        response = self.client.get(self.url)
        # then:
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        

    def test_detail_message_view_for_teacher(self):
        # when:
        self.client.force_authenticate(self.teacher_one.user)
        self.url = reverse('messages-detail', args=[self.child_one.id])
        response = self.client.get(self.url)

        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["child"], self.child_one.id)
        self.assertNotEqual(response.data['child'], self.child_two.id)
    
    def test_detail_message_view_for_parent(self):
        # when:
        self.client.force_authenticate(self.parent.user)
        self.url = reverse('messages-detail', args=[self.child_one.id])
        response = self.client.get(self.url)
        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.messages_child_one.child.id, response.data['child'])        
        self.assertNotEqual(self.messages_child_two.child.id, response.data['child'])

    def test_create_message(self):
        # when:
        self.client.force_authenticate(self.parent.user)
        data = {
            'sender': self.parent.user.id, 
            'child': self.child_one.id,
            'message_text': "Example text"
        }
        self.url = reverse('messages-list')
        response = self.client.post(self.url, data)
        # then:
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['sender'], self.parent.user.id)
        self.assertEqual(response.data['child'], self.child_one.id)
        self.assertEqual(response.data['message_text'], 'Example text')

