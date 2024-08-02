from rest_framework import serializers
from blog_api.models import BlogPost, Comment, Profile
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()




class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['first_name', 'last_name']
        model = User

class SimpleBlogSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    class Meta:
        fields = ['title', 'comment_count']
        model = BlogPost


    def get_comment_count(self, obj):
        return obj.blog_comments.count()
    

class ProfileSerializer(serializers.ModelSerializer):
    blogs = SimpleBlogSerializer(read_only=True, many=True)
    class Meta:
        fields = ['user', 'bio', 'profile_pic', 'blogs']
        model = Profile




class SimpleProfileSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    class Meta:
        fields = ['user_id', 'user', 'profile_pic']
        model = Profile


class CommentSerializer(serializers.ModelSerializer):
    author = SimpleProfileSerializer(read_only=True)
    class Meta:
        fields = ['content', 'author']
        model = Comment


    def create(self, validated_data):
        obj = Comment.objects.create(author=self.context['user'].profile, blogpost_id=self.context['blogpost_id'], **validated_data)
        return obj
    

class BlogPostSerializer(serializers.ModelSerializer):
    author = SimpleProfileSerializer(read_only=True)
    blog_comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        fields = ['title', 'content', 'author', 'blog_comments']
        model = BlogPost


    def create(self, validated_data):
        obj = BlogPost.objects.create(author=self.context['user'].profile, **validated_data)
        return obj
