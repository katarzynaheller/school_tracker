from django.db import models

class DayPlanManager(models.Manager):
    def fetch_by_child_id(self, child_id: int):
        """
        Group dayplans by child_id
        """
        return self.filter(child=child_id)
    
    def fetch_by_child_and_date(self, child_id: int, date):
        """
        Group dayplans by date for given child
        """
        return self.filter(child=child_id, day=date)