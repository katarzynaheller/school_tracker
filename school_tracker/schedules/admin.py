from django.contrib import admin
from .models import DayPlan, Event


@admin.register(DayPlan)
class DayPlanAdmin(admin.ModelAdmin):
    list_display = (
        "child",
        "day",
    )
    ordering = ["day"]
    list_filter = ["child", "day"]
    index_together = ["child", "day"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "date",
    )
    ordering = ["date"]
