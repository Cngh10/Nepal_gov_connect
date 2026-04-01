from django.urls import path
from .views import (
    RegisterView, LoginView, UserProfileView,
    FeedListView, ComplaintActionView, MessageListView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

# Profile
path('profile/', UserProfileView.as_view(), name='profile'),

# Feed & Complaints
path('feed/', FeedListView.as_view(), name='feed'),
path('complaint/<int:pk>/resolve/', ComplaintActionView.as_view({'patch': 'resolve'}), name='complaint-resolve'),
path('complaint/<int:pk>/reply/', ComplaintActionView.as_view({'post': 'reply'}), name='complaint-reply'),

# Messaging
path('messages/', MessageListView.as_view(), name='messages'),

]