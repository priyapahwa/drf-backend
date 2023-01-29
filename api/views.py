from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import transaction

from api.models import Post, User, Notification
from api.serializers import PostSerializer, UserSerializer, NotificationSerializer


'''
The `RegisterView` class is used to register a new user.
The view is a `CreateAPIView` which means it only supports the `POST` method.
It queries the `User` model and uses the `UserSerializer` to serialize the data.
'''
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    '''
    The `post` method is overriden to check if the username, password, and email are provided.
    If they are not provided, a `ValidationError` is raised.
    If they are provided, a new user is created and an invitation email is sent to the user with username and password to create posts.
    '''
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


'''
The `PostViewSet` class is used to create, read, update, and delete posts.
The view is a `ModelViewSet` which means it supports the `GET`, `POST`, `PUT`, `PATCH`, and `DELETE` methods.
It queries the `Post` model and uses the `PostSerializer` to serialize the data.
The viewset inludes the `DjangoFilterBackend` to filter the posts by `status` and `is_archived`.
The viewset also includes the `IsAuthenticated` permission class to ensure that only authenticated users can access the viewset.
'''
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "is_archived"]
    permission_classes = [permissions.IsAuthenticated]

    '''
    The `get_serializer_context` method is overriden to get the serializer 
    context and add the key `posted_by` and value of request user to the context.
    '''
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"posted_by": self.request.user})
        return context

    '''
    The `get_queryset` method is overriden to check if the user is a superuser.
    If the user is not a superuser, the queryset is filtered to only return posts created by the user.
    If the user is a superuser, the queryset returns all posts.
    '''
    def get_queryset(self):
        if not self.request.user.is_superuser:
            return Post.objects.filter(posted_by=self.request.user)

        return Post.objects.all()

    '''
    The `create`, `update`, and `destroy` methods are overriden to create a notification for the user.
    The methods wrap the `super` method in a `transaction.atomic` block to ensure that the notification is created only if the post is created, updated, or deleted.
    Upon calling the `super` method, the `response` variable is assigned the response from the `super` method.
    The `post` variable is assigned the post that was created, updated, or deleted.
    A new notification is created with the `post`, `user`, and `action` fields.
    The `action` field is set to `created`, `updated`, or `deleted` depending on the method.
    The `response` variable is returned from the parent class's method.
    '''
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


'''
The `NotificationView` class is used to view all notifications.
The view is a `ListAPIView` which means it only supports the `GET` method.
It queries the `Notification` model and uses the `NotificationSerializer` to serialize the data.
'''
class NotificationView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    '''
    The `get_queryset` method is overriden to check if the user is a superuser.
    If the user is not a superuser, a `ValidationError` is raised.
    '''
    def get_queryset(self):
        if not self.request.user.is_superuser:
            raise ValidationError("Unauthorized view.")
        return Notification.objects.all()