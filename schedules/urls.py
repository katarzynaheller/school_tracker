from django.urls import path

from .views import DayPlanDailyListView, DayPlanDetailView

urlpatterns = [
    # list view for all children on current day - visible for teacher
    path("", DayPlanDailyListView.as_view(), name="daily_list"),
    # detail view for each child's dayplan - visible for parent (only own child) and teacher
    path("child/<int:pk>/<str:day>/", DayPlanDetailView.as_view(), name="daily_detail"),
]
