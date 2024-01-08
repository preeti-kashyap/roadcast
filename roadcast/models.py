from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils import timezone

class UserProfile(AbstractUser):
    username = models.CharField(unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

class FriendRequest(models.Model):
    from_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sent_friend_requests')
    to_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='received_friend_requests')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
    created_at = models.DateTimeField( default=timezone.now)

    def __str__(self):
        return f"{self.from_user} to {self.to_user} ({self.status})"

