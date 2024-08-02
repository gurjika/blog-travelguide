from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from .permissions import IsCreatorOfBlogOrReadOnly, IsCurrentUserOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from blog_api.serializers import BlogPostSerializer, CommentSerializer, ProfileSerializer, SimpleProfileSerializer
from .models import BlogPost, Profile, Comment
# Create your views here.


class BlogViewSet(ModelViewSet):
    permission_classes = [IsCreatorOfBlogOrReadOnly, IsAuthenticatedOrReadOnly]
    queryset = BlogPost.objects.prefetch_related('blog_comments__author__user', 'blog_comments').select_related('author__user').all()
    serializer_class = BlogPostSerializer

    def get_serializer_context(self):
        return {'user': self.request.user, 'request': self.request}
    
class CommentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(blogpost_id=self.kwargs['blog_pk']).select_related('author__user')
    
    def get_serializer_context(self):
        return {'user': self.request.user, 'blogpost_id': self.kwargs['blog_pk']}
    

class ProfileView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsCurrentUserOrReadOnly]

    def get_object(self):
        username = self.kwargs['username']
        return get_object_or_404(Profile.objects.prefetch_related('blogs__blog_comments').prefetch_related('comments').select_related('user'), user__username=username)