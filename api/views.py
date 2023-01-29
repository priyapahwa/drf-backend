from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import transaction

from api.models import Post, User, Notification
from api.serializers import PostSerializer, UserSerializer, NotificationSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        if not username or not password or not email:
            raise ValidationError("Username, password, and email are required.")
        user = User.objects.create_user(username=username, password=password)
        send_mail(
            'Invitation', 
            'You have been invited to create posts. Here is your username: ' + username + ' and password: ' + password, 
            'testbackend0101@gmail.com', 
            [email], 
            fail_silently=False,
        )
        return Response({"message": "User created and email sent successfully."})

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

    def create(self, request, *args, **kwargs):

        with transaction.atomic():
            response = super().create(request, *args, **kwargs)
            post = Post.objects.get(id=response.data.get("id"))
            Notification.objects.create(
                post = post,
                user = request.user,
                action = "created"
            )
            return response

    def update(self, request, *args, **kwargs):
        with transaction.atomic():
            response = super().update(request, *args, **kwargs)
            post = Post.objects.get(id=response.data.get("id"))
            Notification.objects.create(
                post = post,
                user = request.user,
                action = "updated"
            )
            return response

    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            response = super().destroy(request, *args, **kwargs)
            post = None
            Notification.objects.create(
                post = post,
                user = request.user,
                action = "deleted"
            )
            return response

class NotificationView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_superuser:
            raise ValidationError("Unauthorized view.")
        return Notification.objects.all()