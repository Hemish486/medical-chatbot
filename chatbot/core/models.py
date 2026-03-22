from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("patient", "Patient"),
        ("doctor", "Doctor"),
        ("admin", "Admin"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="patient")
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_history")
    user_message = models.TextField()
    bot_reply = models.TextField()
    source = models.CharField(max_length=20, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} @ {self.created_at:%Y-%m-%d %H:%M}"
