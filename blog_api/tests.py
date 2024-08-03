from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import BlogPost, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class BlogViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.blog_post = BlogPost.objects.create(title='Test Blog', content='This is a test blog.', author=self.user.profile)
        self.url = reverse('blog-list')

    def test_list_blogs(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_blog(self):
        self.client.login(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        data = {'title': 'New Blog', 'content': 'This is a new blog.'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class CommentViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.blog_post = BlogPost.objects.create(title='Test Blog', content='This is a test blog.', author=self.user.profile)
        self.comment = Comment.objects.create(content='Test Comment', author=self.user.profile, blogpost=self.blog_post)
        self.url = reverse('comment-list', kwargs={'blog_pk': self.blog_post.pk})

    def test_list_comments(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_comment(self):
        self.client.login(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        data = {'content': 'New Comment'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ProfileViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('user-profile', kwargs={'username': self.user.username})

    def test_get_profile(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_profile(self):

        self.client.login(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        data = {'bio': 'Updated bio'}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.bio, 'Updated bio')
