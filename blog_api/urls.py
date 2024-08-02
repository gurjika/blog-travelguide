from rest_framework_nested import routers
from . import views
from django.urls import include, path

router = routers.DefaultRouter()


router.register(prefix='blogs', viewset=views.BlogViewSet, basename='blog')

comment_router = routers.NestedDefaultRouter(parent_router=router, parent_prefix='blogs', lookup='blog')
comment_router.register(prefix='comments', viewset=views.CommentViewSet, basename='comment')

urlpatterns = router.urls + comment_router.urls


urlpatterns += [
    path('profile/<str:username>/', views.ProfileView.as_view(), name='user-profile'),
]