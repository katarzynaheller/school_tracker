from django.contrib import admin

from .models import Child, Parent, Teacher, Group


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ("full_name", "parent")


admin.site.register(Parent)
admin.site.register(Teacher)
admin.site.register(Group)



