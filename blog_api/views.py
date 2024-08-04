from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from .permissions import IsCreatorOfObjOrReadOnly, IsCurrentUserOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from blog_api.serializers import BlogPostSerializer, CommentSerializer, ProfileSerializer
from .models import BlogPost, Profile, Comment
from .pagination import DefaultPagination

class BlogViewSet(ModelViewSet):

    """
    ViewSet for managing blog posts.

    This view provides operations to list, create, retrieve, update, and delete blog posts.

    - `permission_classes`: Allows read-only access to unauthenticated users, and only the creator can modify the blog posts.
    - `serializer_class`: Uses `BlogPostSerializer` for GET and POST requests.
    - `get_queryset`: Returns all blog posts with prefetch and select related fields for optimized queries.
    - `get_serializer_context`: Adds the user and request to the serializer context.
    """
    pagination_class = DefaultPagination
    permission_classes = [IsCreatorOfObjOrReadOnly, IsAuthenticatedOrReadOnly]
    queryset = BlogPost.objects.prefetch_related('blog_comments__author__user', 'blog_comments').select_related('author__user').all()
    serializer_class = BlogPostSerializer

    def get_serializer_context(self):
        """
        Return the context for the serializer, including the user and request.
        """
        return {'user': self.request.user, 'request': self.request}
    
class CommentViewSet(ModelViewSet):

    """
    ViewSet for managing comments on blog posts.

    This view provides operations to list, create, retrieve, update, and delete comments for a specific blog post.

    - `permission_classes`: Allows read-only access to unauthenticated users, and only the creator can modify the comments.
    - `serializer_class`: Uses `CommentSerializer` for GET and POST requests.
    - `get_queryset`: Returns comments related to a specific blog post.
    - `get_serializer_context`: Adds the user, blog post ID, and request to the serializer context.
    """
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticatedOrReadOnly, IsCreatorOfObjOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        """
        Return the list of comments for the specific blog post.
        """
        return Comment.objects.filter(blogpost_id=self.kwargs['blog_pk']).select_related('author__user')
    
    def get_serializer_context(self):
        return {'user': self.request.user, 'blogpost_id': self.kwargs['blog_pk'], 'request': self.request}
    

class ProfileView(RetrieveUpdateAPIView):
    """
    View for managing user profiles.

    This view provides operations to retrieve and update a user profile.

    - `permission_classes`: Ensures that only the current user can modify their own profile.
    - `serializer_class`: Uses `ProfileSerializer` for GET and PATCH/PUT requests.
    - `get_object`: Retrieves the profile for the specified username.
    """
    http_method_names = ['get', 'patch', 'head', 'options', 'put']
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsCurrentUserOrReadOnly]

    def get_object(self):
        """
        Return the profile for the specified username.
        """
        username = self.kwargs['username']
        return get_object_or_404(Profile.objects.prefetch_related('blogs__blog_comments').prefetch_related('comments').select_related('user'), user__username=username)