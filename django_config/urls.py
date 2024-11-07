
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
)

from school_tracker.accounts.views import UserViewSet
from school_tracker.chats.views import MessageViewSet
from school_tracker.members.views import MembersViewSet
from school_tracker.schedules.views import DayPlanViewSet


router = routers.SimpleRouter()
router.register(r'accounts', UserViewSet, basename="accounts")
router.register(r'chats', MessageViewSet, basename="messages")
router.register(r'dayplans', DayPlanViewSet, basename="dayplans")
router.register(r'members', MembersViewSet, basename="members")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui')
]

app_name="api"
