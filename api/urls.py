from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import PostViewSet, RegisterView, NotificationView, ArchivePostView

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="posts")

urlpatterns = [
    path("", include(router.urls)),

    path("register/", RegisterView.as_view(), name="register"),
    path("notifications/", NotificationView.as_view(), name="notifications"),
    path("archive/<int:post_id>/", ArchivePostView.as_view(), name="archive"),
]
