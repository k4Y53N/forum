from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.TestView.as_view(), name='test'),
    path('topics/', views.TopicListView.as_view(), name='topic-list'),
    path('topics/<int:topic_id>/posts/', views.TopicPostListView.as_view(), name='topic-detail'),
    path('posts/<int:post_id>/', views.PostDetailView.as_view(), name='post-detail')
]
