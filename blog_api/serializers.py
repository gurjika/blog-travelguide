from rest_framework import serializers
from blog_api.models import BlogPost, Comment, Profile
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['first_name', 'last_name']
        model = User



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['content', 'author']
        model = Comment


class SimpleProfileSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    class Meta:
        fields = ['user_id', 'user', 'profile_pic']
        model = Profile


class BlogPostSerializer(serializers.ModelSerializer):
    author = SimpleProfileSerializer(read_only=True)
    blog_comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        fields = ['title', 'content', 'author', 'blog_comments']
        model = BlogPost


    def create(self, validated_data):
        obj = BlogPost.objects.create(author=self.context['user'].profile, **validated_data)
        return obj
