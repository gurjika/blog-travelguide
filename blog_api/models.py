from django.db import models

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField('core.user', related_name='profile', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', null=True)

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(Profile, related_name='blogs', on_delete=models.CASCADE)
    

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(Profile, related_name='comments', on_delete=models.CASCADE)
    blogpost = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='blog_comments')

    