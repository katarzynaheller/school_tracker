
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from drf_spectacular.views import SpectacularAPIView

from school_tracker.accounts.views import UserViewSet
from school_tracker.chats.views import MessageViewSet
from school_tracker.schedules.views import DayPlanViewSet
from school_tracker.members.views import MembersViewSet


router = routers.SimpleRouter()
router.register(r'accounts', UserViewSet, basename="accounts")
router.register(r'chats', MessageViewSet, basename="messages")
router.register(r'dayplans', DayPlanViewSet, basename="dayplans")
router.register(r'members', MembersViewSet, basename="members")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema")
    # path("api/v1/chats/", include("school_tracker.chats.urls")),
    # path("api/v1/dayplans/", include("school_tracker.schedules.urls")),
    # path("api/v1/members/", include("school_tracker.members.urls")), 
]

app_name="api"
urlpatterns = router.urls
