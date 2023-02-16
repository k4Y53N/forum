from django.urls import path
from . import views

urlpatterns = [
    path('topics/', views.TopicListView.as_view(), name='topic-list'),
    path('topics/<int:topic_id>/posts/', views.TopicPostListView.as_view(), name='topic-detail'),
    path('posts/', views.PostListView.as_view(), name='post-list'),
    path('posts/<int:post_id>/', views.PostDetailView.as_view(), name='post-detail')
]
