from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.views import (
    HomeView, FeedView, SubmitComplaintView, ProfileView, 
    LoginViewTemplate, MessagesView, NotificationsView, 
    ConnectionsView, ComplaintDetailView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('submit_complaint/', SubmitComplaintView.as_view(), name='submit_complaint'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', LoginViewTemplate.as_view(), name='login'),
    path('messages/', MessagesView.as_view(), name='messages'),
    path('notifications/', NotificationsView.as_view(), name='notifications'),
    path('connections/', ConnectionsView.as_view(), name='connections'),
    path('complaint_detail/<int:pk>/', ComplaintDetailView.as_view(), name='complaint_detail'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), # Connect to your API routes
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)