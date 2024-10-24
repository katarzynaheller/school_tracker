from django.db import models

class MessageManager(models.Manager):
    def fetch_by_child_id(self, child_id: int):
        """
        Fetch messages by child_id
        """
        return self.filter(child=child_id)
    
    def fetch_by_sender_id(self, sender_id: int):
        """
        Fetch messages by sender
        """
        return self.filter(sender=sender_id)

    def fetch_by_sender_and_child(self, sender_id: int, child_id: int):
        """
        Fetch messages for sender's particular child
        """
        return self.filter(sender=sender_id, child_id=child_id)
    
    def fetch_by_date(self, child_id: int, date):
        """
        Fetch messages about particular child for a particular day
        """
        return self.filter(child=child_id, timestamp__date=date)