from django.db import models

class MessageManager(models.Manager):
    def fetch_by_child_id(self, child_id: int):
        """
        Group messages by child_id
        """
        return self.filter(child=child_id)
    
    def fetch_by_sender_id(self, sender_id: int):
        """
        Group messages by sender
        """
        return self.filter(sender=sender_id)
    
    def fetch_by_date(self, child_id: int, date):
        """
        Group messages by date
        """
        return self.filter(child=child_id, timestamp__date=date)