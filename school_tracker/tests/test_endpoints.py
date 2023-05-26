from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .factories import CustomUserFactory, ParentFactory, ChildFactory, TeacherFactory, GroupFactory, MessageFactory

class CheckPermissionForEndpoints(APITestCase):

    #accessible for teacher, not parent (members/children/)
    def test_access_to_child_list_view_for_teacher(self):
        self.url = reverse('children_list')

        user = CustomUserFactory()
        teacher = TeacherFactory()
        parent = ParentFactory()

        child = ChildFactory(parent = parent)

        self.client.force_authenticate(user=teacher)
        responce = self.client.get(self.url)

        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        pass
        

    def test_access_to_child_list_view_for_parent(self):
        self.url = reverse('children_list')
        pass

    #accessible for related teacher and parent (members/child/1/)
    def test_access_to_child_detail_view(self):
        self.url = reverse('child_detail')
        pass

    #accessible for all members with is_staff status (teachers) (members/group/)
    def test_group_list_view(self):
        self.url = reverse('group_list')
        pass

    #accessible only for a related teacher (members/group/1/)
    def test_group_detail_view(self):
        # self.url = reverse('group_detail')
        pass

    #accessible for all members with is_staff status (teachers) (members/parent/)
    def test_parent_list_view(self):
        self.url = reverse('parent_list')
        pass

    #accessible for owner and is_staff members (members/parent/1/)
    def test_parent_detail_view(self):
        self.url = reverse('parent_list')
        pass

    #accessible for related parent and teacher but with different queryset (chats/)
    def test_access_to_message_main_view(self):
        self.url = reverse('message_main_list')
        pass
    
    #accessible for users related with particular child (chats/child/1/)
    def test_access_to_message_detailed_view(self):
        # self.url = reverse('message_detailed_list')
        pass