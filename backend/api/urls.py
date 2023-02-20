from django.urls import path
from . import views

urlpatterns = [
    path('topics/', views.TopicListView.as_view()),
    path('topics/<int:topic_id>/posts/', views.TopicPostListView.as_view()),
    path('posts/', views.PostListView.as_view()),
    path('posts/<int:post_id>/', views.PostDetailView.as_view()),
    path('posts/<int:post_id>/replies/', views.PostReplyListView.as_view()),
    path('replies/', views.ReplyListView.as_view()),
    path('replies/<int:reply_id>/', views.ReplyDetailView.as_view()),
    path('replies/<int:reply_id>/comments/', views.ReplyCommentListView.as_view()),
    path('comments/', views.CommentListView.as_view()),
    path('comments/<int:comment_id>/', views.CommentDetailView.as_view())
]
