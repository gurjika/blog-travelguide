from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from blog_api.serializers import BlogPostSerializer
from .models import BlogPost, Profile, Comment
# Create your views here.


class BlogViewSet(ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def get_serializer_context(self):
        return {'user': self.request.user}