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

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    theme = models.CharField(max_length=10, default="dark")
    font_size = models.CharField(max_length=10, default="16px")

    autoplay = models.BooleanField(default=False)
    subtitles = models.BooleanField(default=True)

    data_saver = models.BooleanField(default=False)

    notification_sound = models.BooleanField(default=True)
    vibration = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Settings"        
