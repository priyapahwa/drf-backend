from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import PostViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="posts")

urlpatterns = [
    path("", include(router.urls)),
]
