from django.urls import path
from .views import MessageCreateAPIView, MessageMainListAPIView, MessageDetailedListView



urlpatterns = [
    path('', MessageMainListAPIView.as_view(), name="message_main_list"),
    path('child/<int:child_id>/', MessageDetailedListView.as_view(), name="message_detailed_list"),
    path('create/', MessageCreateAPIView.as_view(), name="message_create"),
    
]
