from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.models import Post, User, Notification

'''
The `UserSerializer` class is used to serialize the `User` model.
Attributes:
    Meta: A nested class that contains the model and fields to be serialized.
    model: The model to be serialized.
    fields: The fields to be serialized (id, username, password, email)
Methods:
    create: Creates a new user with given validated data.
'''
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password", "email")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


'''
The `PostSerializer` class is used to serialize the `Post` model.
Attributes:
    Meta: A nested class that contains the model and fields to be serialized.
    model: The model `Post` to be serialized.
    fields: The fields to be serialized (id, title, description, created_at, updated_at, status, is_archived)
    read_only_fields: The fields that are read only (id, created_at, updated_at)
Methods:
    create: The `create` method is overridden to set the `posted_by` field in the context.
'''
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "status",
            "is_archived",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        posted_by = self.context["posted_by"]
        post = Post.objects.create(posted_by=posted_by, **validated_data)
        return post


'''
The `NotificationSerializer` class is used to serialize the `Notification` model.
Attributes:
    Meta: A nested class that contains the model and fields to be serialized.
    model: The model `Notification` to be serialized.
    fields: The fields to be serialized (id, post, user, action)
    where `action` refers to create, update, or delete.
'''
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "post", "user", "action"]

