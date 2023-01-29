from django.contrib.auth.models import User
from django.db import models

STATUS = (
    ("draft", "Draft"),
    ("published", "Published"),
)


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

class Notification(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    action_at = models.DateTimeField(auto_now_add=True)