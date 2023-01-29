from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response

from api.models import Post, User
from api.serializers import PostSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "is_archived"]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"posted_by": self.request.user})
        return context

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return Post.objects.filter(posted_by=self.request.user)

        return Post.objects.all()
