from django.urls import path

from .views import ChildListView, ChildDetailView, ParentListView, ParentDetailView, GroupDetailView, GroupListView

urlpatterns = [
    path("children/", ChildListView.as_view(), name="children_list"),
    path("child/<int:pk>/", ChildDetailView.as_view(), name="child_detail"),
    path("group/", GroupListView.as_view(), name="group_list"),
    path("group/<int:pk>/", GroupDetailView.as_view(), name="group_detail"),
    path("parent/", ParentListView.as_view(), name="parent_list"),
    path("parent/<int:pk>/", ParentDetailView.as_view(), name="parent_detail"),
]
