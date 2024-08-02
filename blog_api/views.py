from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from .permissions import IsCreatorOfBlogOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from blog_api.serializers import BlogPostSerializer, CommentSerializer
from .models import BlogPost, Profile, Comment
# Create your views here.


class BlogViewSet(ModelViewSet):
    permission_classes = [IsCreatorOfBlogOrReadOnly, IsAuthenticatedOrReadOnly]
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def get_serializer_context(self):
        return {'user': self.request.user}
    
class CommentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(blogpost_id=self.kwargs['blog_pk'])
    
    def get_serializer_context(self):
        return {'user': self.request.user, 'blogpost_id': self.kwargs['blog_pk']}
    

