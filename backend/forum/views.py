from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from . import forms
from .models import *

# Create your views here.


class Home(View):
    def get(self, request):
        topics = Topic.objects.all()[:10]
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

    @method_decorator(login_required(redirect_field_name='next', login_url='/login/'))
    def post(self, request):
        form = forms.TopicForm(data=request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest(form.errors.as_text())
        topic = form.save()

        return redirect(reverse('topic-detail', kwargs={'topic_id': topic.id}))


class TopicDetail(View):
    def get(self, request, topic_id):
        topic = get_object_or_404(Topic, pk=topic_id)
        posts = Post.objects.filter(topic=topic, content__isnull=False)[:10]
        context = {
            'topic': topic,
            'posts': posts
        }

        return render(request, 'topic-detail.html', context)


class PostList(View):
    def get(self, request, topic_id):
        topic = get_object_or_404(Topic, pk=topic_id)
        posts = Post.objects.select_related('user').filter(topic=topic)
        context = {
            'topic': topic,
            'posts': posts
        }

        return render(request, 'post-list.html', context)

    @method_decorator(login_required(redirect_field_name='next', login_url='/login/'))
    def post(self, request, topic_id):
        topic = get_object_or_404(Topic, pk=topic_id)
        form = forms.PostCreateForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest(form.errors.as_text())
        clean_data = form.cleaned_data
        title = clean_data['title']
        context = clean_data['context']
        user = request.user
        post = Post.objects.create(topic=topic, title=title, user=user)
        Content.objects.create(post=post, user=user, text=context)

        return redirect(
            reverse(
                'post-detail',
                kwargs={
                    'post_id': post.id
                }
            )
        )


class PostDetail(View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id, content__isnull=False)
        replies = post.replies.all()
        context = {
            'post': post,
            'replies': replies
        }

        return render(request, 'post-detail.html', context=context)


class ReplyList(View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        form = forms.ReplyCreateForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest(form.errors.as_text())
        content: Content = form.save(commit=False)
        content.reply = post
        content.user = request.user
        content.save()

        return redirect(reverse('post-detail', kwargs={'post_id': post.id}))


class CommentList(View):
    def post(self, request, reply_id):
        content = get_object_or_404(Content, pk=reply_id)
        form = forms.CommentCreateForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest(form.errors.as_text())
        comment = form.save(commit=False)
        comment.content = content
        comment.user = request.user
        comment.save()
        if content.is_context():
            post_id = content.post.id
        else:
            post_id = content.reply.id

        return redirect(reverse('post-detail', kwargs={'post_id': post_id}))
