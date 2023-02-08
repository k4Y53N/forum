from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:user_id>/', views.UserDetail.as_view(), name='user-detail'),
    path('topics/', views.TopicList.as_view(), name='topic-list'),
    path('topics/<int:topic_id>/', views.TopicDetail.as_view(), name='topic-detail'),
    path('topics/<int:topic_id>/posts/', views.PostList.as_view(), name='post-list'),
    path('topics/<int:topic_id>/posts/<int:post_id>/', views.PostDetail.as_view(), name='post-detail'),
]