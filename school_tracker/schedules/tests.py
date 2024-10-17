from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import date

from members.models import Child, Parent
from .models import DayPlan


class DayPlanTests(TestCase):
    @classmethod
    def setUp(cls):
        cls.user = get_user_model().objects.create_user(
            email="testparent@mail.com", password="secret"
        )

        cls.parent = Parent.objects.create(user=cls.user)
        cls.child = Child.objects.create(
            full_name="Test Child",
            birth_date=date(2022, 3, 6),
            parent=cls.parent,
        )

        cls.dayplan = DayPlan.objects.create(
            child=cls.child,
            day=timezone.now().date(),
            summary="everything ok",
        )

    def test_dayplan_model(self):
        self.assertEqual(self.dayplan.child.full_name, "Test Child")
        self.assertEqual(self.dayplan.summary, "everything ok")
        self.assertEqual(self.dayplan.day, timezone.now().date())
