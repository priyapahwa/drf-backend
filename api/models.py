from django.contrib.auth.models import User
from django.db import models

STATUS = (
    ("draft", "Draft"),
    ("published", "Published"),
)

'''
The `Post` model represents a post created by users related to the `User` model.
Attributes:
    title: The title of the post.
    description: The description of the post.
    created_at: The date and time when the post was created. (auto-populated)
    updated_at: The date and time when the post was last updated. (auto-poulated)
    posted_by: The user who created the post. This is linked to User by a foreign key.
    status: The status of the post. This is a choice field with two options: draft and published.
    is_archived: A boolean field that determines whether the post is archived or not.
Methods:
    __str__: Returns the title of the post.
'''
class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10, choices=STATUS, null=False, default="draft"
    )

    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title


'''
The `Notification` model represents notifications of various actions by users.
Attributes:
    post: The post that the notification is related to.
    user: The user who created the notification.
    action: The action that the notification is related to such as "created", "updated", "deleted".
    action_at: The date and time when the action was performed. (auto-populated)
'''
class Notification(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    action_at = models.DateTimeField(auto_now_add=True)