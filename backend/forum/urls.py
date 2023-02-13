from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('users/<int:user_id>/', views.UserDetail.as_view(), name='user-detail'),
    path('topics/', views.TopicList.as_view(), name='topic-list'),
    path('topics/<int:topic_id>/', views.TopicDetail.as_view(), name='topic-detail'),
    path('topics/<int:topic_id>/posts/', views.PostList.as_view(), name='post-list'),
    path('posts/<int:post_id>/', views.PostDetail.as_view(), name='post-detail'),
    path('posts/<int:post_id>/replies/', views.ReplyList.as_view(), name='reply-list'),
    path('replies/<int:reply_id>/comments/', views.CommentList.as_view(), name='comment-list'),
]