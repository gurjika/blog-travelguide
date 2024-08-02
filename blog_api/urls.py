from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()


router.register(prefix='blogs', viewset=views.BlogViewSet, basename='blog')

comment_router = routers.NestedDefaultRouter(parent_router=router, parent_prefix='blogs', lookup='blog')
comment_router.register(prefix='comments', viewset=views.CommentViewSet, basename='comment')

urlpatterns = router.urls + comment_router.urls