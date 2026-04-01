from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView
from .models import User, FeedItem, Message
from .serializers import UserSerializer, FeedItemSerializer, MessageSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

class LoginView(TokenObtainPairView):
    # Standard JWT Login
    pass

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def get_object(self):
    return self.request.user

class FeedListView(generics.ListCreateAPIView):
    queryset = FeedItem.objects.all().order_by('-timestamp')
    serializer_class = FeedItemSerializer
    permission_classes = (permissions.AllowAny,)  # Allow anonymous submissions for prototype

    def perform_create(self, serializer):
        # For prototype, use a default user if not authenticated
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            user, created = User.objects.get_or_create(
                username='anonymous',
                defaults={
                    'email': 'anon@example.com',
                    'role': 'PUBLIC'
                }
            )
        serializer.save(user=user, type='COMPLAINT')

class ComplaintActionView(viewsets.ViewSet):
    """
    Handles Government-only actions on complaints.
    """

def resolve(self, request, pk=None):
    if request.user.role != 'GOVERNMENT':
        return Response({"error": "Only officials can resolve complaints."}, status=status.HTTP_403_FORBIDDEN)
        
    complaint = get_object_or_404(FeedItem, pk=pk, type='COMPLAINT')
    complaint.status = 'RESOLVED'
    complaint.save()
    return Response({"status": "Complaint marked as resolved."})

def reply(self, request, pk=None):
    if request.user.role != 'GOVERNMENT':
        return Response({"error": "Only officials can reply to complaints."}, status=status.HTTP_403_FORBIDDEN)
        
    complaint = get_object_or_404(FeedItem, pk=pk, type='COMPLAINT')
    reply_text = request.data.get('text')
    
    # In a real app, you'd create a Comment model. 
    # For this prototype, we'll simulate a reply by updating content or adding a log.
    return Response({"status": "Reply posted to complaint.", "reply": reply_text})

class MessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

def get_queryset(self):
    # Only see messages where the user is either the sender or receiver
    user = self.request.user
    return Message.objects.filter(sender=user) | Message.objects.filter(receiver=user)

def perform_create(self, serializer):
    serializer.save(sender=self.request.user)


class HomeView(TemplateView):
    template_name = 'feed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all complaints ordered by timestamp (newest first)
        context['complaints'] = FeedItem.objects.filter(type='COMPLAINT').order_by('-timestamp')
        return context

class FeedView(TemplateView):
    template_name = 'feed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all complaints ordered by timestamp (newest first)
        context['complaints'] = FeedItem.objects.filter(type='COMPLAINT').order_by('-timestamp')
        return context

class SubmitComplaintView(TemplateView):
    template_name = 'submit_complaint.html'

class ProfileView(TemplateView):
    template_name = 'profile.html'

class LoginViewTemplate(TemplateView):
    template_name = 'login.html'

class MessagesView(TemplateView):
    template_name = 'messages.html'

class NotificationsView(TemplateView):
    template_name = 'notifications.html'

class ConnectionsView(TemplateView):
    template_name = 'connections.html'

class ComplaintDetailView(DetailView):
    model = FeedItem
    template_name = 'complaint_detail.html'
    context_object_name = 'complaint'

