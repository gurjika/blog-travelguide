from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from .permissions import IsCreatorOfObjOrReadOnly, IsCurrentUserOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from blog_api.serializers import BlogPostSerializer, CommentSerializer, ProfileSerializer
from .models import BlogPost, Profile, Comment
from .pagination import DefaultPagination

class BlogViewSet(ModelViewSet):
    pagination_class = DefaultPagination
    permission_classes = [IsCreatorOfObjOrReadOnly, IsAuthenticatedOrReadOnly]
    queryset = BlogPost.objects.prefetch_related('blog_comments__author__user', 'blog_comments').select_related('author__user').all()
    serializer_class = BlogPostSerializer

    def get_serializer_context(self):
        return {'user': self.request.user, 'request': self.request}
    
class CommentViewSet(ModelViewSet):
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsCreatorOfObjOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(blogpost_id=self.kwargs['blog_pk']).select_related('author__user')
    
    def get_serializer_context(self):
        return {'user': self.request.user, 'blogpost_id': self.kwargs['blog_pk'], 'request': self.request}
    

class ProfileView(RetrieveUpdateAPIView):
    http_method_names = ['get', 'patch', 'head', 'options', 'put']
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsCurrentUserOrReadOnly]

    def get_object(self):
        username = self.kwargs['username']
        return get_object_or_404(Profile.objects.prefetch_related('blogs__blog_comments').prefetch_related('comments').select_related('user'), user__username=username)