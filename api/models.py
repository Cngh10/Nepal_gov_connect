from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('PUBLIC', 'Public Citizen'),
        ('GOVERNMENT', 'Government Official'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='PUBLIC')
    is_verified = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

class FeedItem(models.Model):
    TYPE_CHOICES = (
        ('POST', 'Official Announcement'),
        ('COMPLAINT', 'Citizen Complaint'),
    )
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    timestamp = models.DateTimeField(auto_now_add=True)
    location_tag = models.CharField(max_length=255, blank=True, null=True)

class Media(models.Model):
    feed_item = models.ForeignKey(FeedItem, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='feed_media/')
    is_video = models.BooleanField(default=False)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)