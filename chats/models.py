from django.db import models
from accounts.models import CustomUser

from members.models import Child, Group


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
        try:
            child_group = self.child.group_member if self.child else "No Group assigned"
            return f"Message about {self.child}(Group {child_group})"
        except Group.DoesNotExist:
        # Handle the case when the group does not exist
            return f"Message about {self.child} (no assigned group)"
    
    #the most recent messsages appearing first    
    class Meta:
        ordering = ('-timestamp',)



