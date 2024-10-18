
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from drf_spectacular.views import SpectacularAPIView

from school_tracker.chats.views import MessageViewSet


router = routers.SimpleRouter()
# router.register(r'accounts', AccountViewSet, basename="accounts")
router.register(r'chats', MessageViewSet, basename="messages")
# router.register(r'dayplans', DayPlanViewSet, basename="dayplans")
# reouter.register(r'members', MemberViewSet, basename="members")


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
