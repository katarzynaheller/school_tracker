from django.urls import path
from .views import MessageListAPIView, MessageCreateAPIView, MessageDetailAPIView

app_name= "chats"

urlpatterns = [
    path('', MessageListAPIView.as_view(), name="message_list"),
    path('create/', MessageCreateAPIView.as_view(), name="message_create"),
    path('<int:message_id>/', MessageDetailAPIView.as_view(), name="message_detail"),
]
