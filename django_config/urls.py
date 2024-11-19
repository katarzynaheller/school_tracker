
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)

from school_tracker.accounts.views import (
    UserViewSet,
    MeViewSet
)
from school_tracker.chats.views import MessageViewSet
from school_tracker.members.views import (
    ChildViewSet, 
    GroupViewSet,
    MemberViewSet, 
    TeacherViewSet
)
from school_tracker.schedules.views import DayPlanViewSet


router = routers.SimpleRouter()
# User Management
router.register(r'account', UserViewSet, basename="accounts")
router.register(r'me', MeViewSet, basename="me")
# Messages/Chat
router.register(r'chat', MessageViewSet, basename="messages")
# DayPlan
router.register(r'dayplan', DayPlanViewSet, basename="dayplans")
# Members Endpoints
router.register(r'member', MemberViewSet, basename="members")
router.register(r'child', ChildViewSet, basename="children")
router.register(r'group', GroupViewSet, basename="groups")
router.register(r'teacher', TeacherViewSet, basename="teachers")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui')
]

