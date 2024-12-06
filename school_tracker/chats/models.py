from django.db import models

from school_tracker.accounts.models import CustomUser
from school_tracker.chats.manager import MessageManager
from school_tracker.members.models import (
    Child, 
    Group
)


class Message(models.Model):
    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='sent_messages',
    )
    child = models.ForeignKey(Child, on_delete=models.CASCADE, null=True, blank=True)
    message_text = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = MessageManager()

    def __str__(self):
        return f"Message about {self.child.full_name} sent by {self.sender.email}"

    class Meta:
        ordering = ('-timestamp',)


