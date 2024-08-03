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
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        fields = ['user', 'bio', 'profile_pic', 'blogs']
        model = Profile

    def get_profile_pic(self, obj):
        if obj.profile_pic:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.profile_pic.url)
        return None


class SimpleProfileSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        fields = ['user_id', 'user', 'profile_pic']
        model = Profile

    def get_profile_pic(self, obj):
        if obj.profile_pic:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.profile_pic.url)
        return None


class CommentSerializer(serializers.ModelSerializer):
    author = SimpleProfileSerializer(read_only=True)
    class Meta:
        fields = ['content', 'author']
        model = Comment


    def create(self, validated_data):

        obj = Comment.objects.create(author=self.context['user'].profile, blogpost_id=self.context['blogpost_id'], **validated_data)
        return obj
    
    def validate(self, data):
        if not data.get('content', '').strip():
            raise serializers.ValidationError('Content cannot be empty.')
        return data

class BlogPostSerializer(serializers.ModelSerializer):
    author = SimpleProfileSerializer(read_only=True)
    blog_comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    class Meta:
        fields = ['title', 'content', 'author', 'blog_comments', 'comment_count']
        model = BlogPost

    def validate(self, data):
        if not data.get('title', '').strip():
            raise serializers.ValidationError('Title cannot be empty.')
        if not data.get('content', '').strip():
            raise serializers.ValidationError('Content cannot be empty.')
        
        return data
    def get_comment_count(self, obj):
        return obj.blog_comments.count()

    def create(self, validated_data):
        obj = BlogPost.objects.create(author=self.context['user'].profile, **validated_data)
        return obj
