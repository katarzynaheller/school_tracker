from django.db import models
from accounts.models import CustomUser

from members.models import Child


class Message(models.Model):
    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='sent_messages',
    )

    child = models.ForeignKey(Child, on_delete=models.CASCADE, null=True, blank=True)
    message_text = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"about {self.child}"
    
    class Meta:
        ordering = ('timestamp',)



