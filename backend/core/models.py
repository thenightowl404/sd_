from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    type = models.CharField(max_length=20)
    icon = models.CharField(max_length=10, default="🔔")

    text = models.TextField()

    read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]