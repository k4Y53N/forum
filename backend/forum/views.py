from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import *

# Create your views here.


class Home(View):
    def get(self, request):
        topics = Topic.objects.all()[:5]
        context = {
            'topics': topics
        }
        return render(request, 'home.html', context)


class UserList(View):
    def get(self, request):
        pass


class UserDetail(View):
    def get(self, request):
        pass


class TopicList(View):
    def get(self, request):
        topics = Topic.objects.all()
        context = {
            'topics': topics
        }

        return render(request, 'topic-list.html', context)


class TopicDetail(View):
    def get(self, request, topic_id):
        topic = get_object_or_404(Topic, pk=topic_id)
        posts = Post.objects.filter(topic=topic)[:5]
        context = {
            'topic': topic,
            'posts': posts
        }

        return render(request, 'topic-detail.html', context)


class PostList(View):
    def get(self, request, topic_id):
        topic = get_object_or_404(Topic, pk=topic_id)
        posts = Post.objects.filter(topic=topic)
        context = {
            'topic': topic,
            'posts': posts
        }

        return render(request, 'post-list.html', context)


class PostDetail(View):
    def get(self, request, topic_id, post_id):
        post = get_object_or_404(Post, topic__pk=topic_id, pk=post_id)
        replies = post.replies.all()
        context = {
            'post': post,
            'replies': replies
        }

        return render(request, 'post-detail.html', context=context)
