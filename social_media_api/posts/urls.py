from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, user_feed, LikePostView, UnlikePostView

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', user_feed, name='user_feed'),
    path('<int:post_id>/like/', LikePostView.as_view(), name='like_post'),
    path('<int:post_id>/unlike/', UnlikePostView.as_view(), name='unlike_post'),
]