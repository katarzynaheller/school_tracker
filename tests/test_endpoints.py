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
        self.assertIn(self.child, self.group.group_students.all())

    def test_list_child_view_for_parent(self):
        
        # when:
        self.client.force_authenticate(user=self.parent.user)
        response = self.client.get(self.url)

        # then:
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.parent.user.is_staff, False)
        self.assertEqual(self.parent.user.user_type, UserTypeEnum.parent)
        self.assertIn(self.parent, self.child.parents.all())

    def test_detail_child_view_for_parent(self):
    
        # when:
        self.client.force_authenticate(user=self.parent.user)
        self.url = reverse("children-detail", kwargs={"child_id": self.child.id})
        response = self.client.get(self.url)

        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.parent.user.user_type, UserTypeEnum.parent)
        self.assertIn(self.parent, self.child.parents.all())

    def test_detail_child_view_for_unrealted_parent(self):
    
        # when:
        self.client.force_authenticate(user=self.parent_another.user)
        self.url = reverse("children-detail", kwargs={"child_id": self.child.id})
        response = self.client.get(self.url)

        # then:
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_child_view_for_related_teacher(self):

        # when:
        self.client.force_authenticate(user = self.teacher.user)
        self.url = reverse('children-detail', kwargs={"child_id": self.child.id})
        response = self.client.get(self.url)

        # then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.child, self.group.group_students.all())
        self.assertIn(self.teacher, [assigned_teacher.teacher for assigned_teacher in self.group.assigned_teachers.all()])

    def test_detail_view_for_unrelated_teacher(self):

        # when:
        self.client.force_authenticate(user = self.unrelated_teacher.user)
        self.url = reverse('children-detail', kwargs={"child_id": self.child.id})
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
        self.url = reverse('groups-detail', kwargs={"group_id":self.group.id})
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.group.assigned_teachers.first().teacher, self.teacher)
        

    def test_group_detail_view_unrelated_teacher(self):

        # when:
        self.client.force_authenticate(self.unrelated_teacher.user)
        self.url = reverse('groups-detail', kwargs={"group_id":self.group.id})
        response = self.client.get(self.url)

        #assertions
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(self.group.assigned_teachers.first().teacher, self.unrelated_teacher)

    def test_group_detail_view_parent(self):

        # when:
        self.client.force_authenticate(self.parent.user)
        self.url = reverse('groups-detail', kwargs={"group_id":self.group.id})
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    # #Parent ListView accessible for all members with is_staff status (teachers) (members/parent/)
    # def test_parent_list_view_teacher(self):

    #     #set up
    #     user_teacher = CustomUserFactory()
    #     teacher = TeacherFactory(user = user_teacher)
    #     user_parent = CustomUserFactory()
    #     parent = ParentFactory(user = user_parent)

    #     #GET request
    #     self.client.force_authenticate(teacher)
    #     self.url = reverse('parent_list')
    #     response = self.client.get(self.url)
        
    #     #assertions
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIsInstance(response.data, list)

    # def test_parent_list_view_parent(self):

    #     #set up
    #     user_teacher = CustomUserFactory()
    #     teacher = TeacherFactory(user = user_teacher)
    #     user_parent = CustomUserFactory()
    #     parent = ParentFactory(user = user_parent)

    #     #GET request
    #     self.client.force_authenticate(parent)
    #     self.url = reverse('parent_list')
    #     response = self.client.get(self.url)
        
    #     #assertions
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # #Parent DetailView accessible for owner and is_staff members (members/parent/1/)
    # def test_parent_detail_view(self):
        
    #     #set up
    #     user_teacher = CustomUserFactory()
    #     teacher = TeacherFactory(user = user_teacher)
    #     user_parent = CustomUserFactory()
    #     parent = ParentFactory(user = user_parent)

    #     #GET request
    #     self.client.force_authenticate(teacher)
    #     self.url = reverse('parent_detail', args=[parent.id])
    #     response = self.client.get(self.url)
        
    #     #assertions
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertContains(response, user_parent.id)

    # #Message main ListView accessible for related parent and teacher but with different queryset (chats/)
    # def test_access_to_message_main_view_teacher(self):

    #     #set up
    #     user_teacher_one = CustomUserFactory(user_type = CustomUser.TEACHER)
    #     teacher_one = TeacherFactory(user = user_teacher_one)
    #     user_teacher_two = CustomUserFactory(user_type = CustomUser.TEACHER)
    #     teacher_two = TeacherFactory(user = user_teacher_two)
    #     user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
    #     parent = ParentFactory(user = user_parent)
    #     child_one = ChildFactory(parents = [parent])
    #     child_two = ChildFactory(parents = [parent] )
    #     group_child_one = GroupFactory(teacher = teacher_one, members = [child_one])
    #     group_child_two = GroupFactory(teacher = teacher_two, members = [child_two])
    #     message_child_one = MessageFactory(sender = user_parent, child = child_one)
    #     message_child_two = MessageFactory(sender = user_parent, child = child_two)

    #     #GET request
    #     self.client.force_authenticate(user_teacher_one)
    #     self.url = reverse('message_main_list')
    #     response = self.client.get(self.url)

    #     #assertions
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIsInstance(response.data, list)
    #     self.assertContains(response, child_one.id)
    #     self.assertContains(response, message_child_one.id)
    #     self.assertNotContains(response, message_child_two.id)
    #     self.assertEqual(len(response.data), 1)

    # def test_access_to_message_main_view_parent(self):

    #     #set up
    #     user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
    #     parent = ParentFactory(user = user_parent)
    #     child_one = ChildFactory(parents = [parent])
    #     child_two = ChildFactory(parents = [parent])
    #     message_child_one = MessageFactory(sender = user_parent, child = child_one)
    #     message_child_two = MessageFactory(sender = user_parent, child = child_two)

    #     #GET request
    #     self.client.force_authenticate(user_parent)
    #     self.url = reverse('message_main_list')
    #     response = self.client.get(self.url)

    #     #assertions
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIsInstance(response.data, list)
    #     self.assertContains(response, child_one.id)
    #     self.assertContains(response, child_two.id)
    #     self.assertContains(response, message_child_one.id)
    #     self.assertContains(response, message_child_two.id)
    #     self.assertEqual(len(response.data), 2)

    # def test_access_to_message_main_view_unrelated_teacher(self):

    #     #set up
    #     related_user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
    #     related_teacher = TeacherFactory(user = related_user_teacher)
    #     unrelated_user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
    #     unrelated_teacher = TeacherFactory(user = unrelated_user_teacher)
    #     user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
    #     parent = ParentFactory(user = user_parent)
    #     child = ChildFactory(parents = [parent])
    #     group = GroupFactory(teacher = related_teacher, members = [child])
    #     message = MessageFactory(sender = user_parent, child = child)

    #     #GET request
    #     self.client.force_authenticate(unrelated_user_teacher)
    #     self.url = reverse('message_main_list')
    #     response = self.client.get(self.url)

    #     #assertions
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertNotEqual(group.teacher, unrelated_teacher)
    #     self.assertIsInstance(response.data, list)
    #     self.assertEqual(len(response.data), 0)
    

    # #Message detailed ListView accessible for users related with particular child (chats/child/1/)
    # def test_access_to_message_detailed_view_related_teacher(self):

    #     #set up
    #     user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
    #     teacher = TeacherFactory(user = user_teacher)
    #     user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
    #     parent = ParentFactory(user = user_parent)
    #     child = ChildFactory(parents = [parent])
    #     group = GroupFactory(teacher = teacher, members = [child])
    #     message = MessageFactory(sender = user_parent, child = child)

    #     #GET request
    #     self.client.force_authenticate(user_teacher)
    #     self.url = reverse('message_detailed_list', args=[child.id])
    #     response = self.client.get(self.url)

    #     #assertions
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)



    # def test_access_to_message_detailed_view_unrelated_teacher(self):

    #     #set up
    #     related_user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
    #     related_teacher = TeacherFactory(user = related_user_teacher)
    #     unrelated_user_teacher = CustomUserFactory(user_type = CustomUser.TEACHER)
    #     unrelated_teacher = TeacherFactory(user = unrelated_user_teacher)
    #     user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
    #     parent = ParentFactory(user = user_parent)
    #     child = ChildFactory(parents = [parent])
    #     group = GroupFactory(teacher = related_teacher, members = [child])
    #     message = MessageFactory(sender = user_parent, child = child)

    #     #GET request
    #     self.client.force_authenticate(unrelated_user_teacher)
    #     self.url = reverse('message_detailed_list', args=[child.id])
    #     response = self.client.get(self.url)

    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

    # def test_access_to_message_detailed_view_parent(self):

    #     #set up
    #     user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
    #     parent = ParentFactory(user = user_parent)
    #     child_one = ChildFactory(parents = [parent])
    #     child_two = ChildFactory(parent=parent)
    #     message_child_one = MessageFactory(sender = user_parent, child = child_one)
    #     message_child_two = MessageFactory(sender = user_parent, child = child_two)

    #     #GET response
    #     self.client.force_authenticate(user_parent)
    #     self.url = reverse('message_detailed_list', args=[child_one.id])
    #     response = self.client.get(self.url)

    #     #assertions
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data),1)
    #     self.assertIn(message_child_one.message_text, [message['message_text'] for message in response.data])        
    #     self.assertNotIn(message_child_two.message_text, [message['message_text'] for message in response.data])

    # def test_create_message(self):
        
    #     #set up
    #     user_parent = CustomUserFactory(user_type = CustomUser.PARENT)
    #     parent = ParentFactory(user = user_parent)
    #     child = ChildFactory(parent=parent)
    #     message_text = 'Hello, this is a test message'

    #     #POST request
    #     self.client.force_authenticate(user_parent)
    #     data = {
    #         'child':child.id,
    #         'message_text': message_text
    #     }
    #     self.url = reverse('message_create')
    #     response = self.client.post(self.url, data)

    #     created_message = Message.objects.latest("id")

    #     #assertions
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(created_message.sender, user_parent)
    #     self.assertEqual(created_message.child, child)
    #     self.assertEqual(created_message.message_text, message_text)

