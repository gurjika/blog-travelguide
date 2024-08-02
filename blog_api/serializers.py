from rest_framework import serializers

from blog_api.models import BlogPost, Comment, Profile


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['content', 'author']
        model = Comment


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['user', 'bio', 'profile_pic', 'blogs']
        model = Profile


class BlogPostSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    blog_comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        fields = ['title', 'content', 'author', 'blog_comments']
        model = BlogPost


    def create(self, validated_data):

        obj = BlogPost.objects.create(author=self.context['user'].profile, **validated_data)
        return obj
