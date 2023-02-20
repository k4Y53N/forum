from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from forum.models import Topic, Post, Content, Comment
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwner
from . import filters
from . import serializers


# Create your views here.

class TopicListView(generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = serializers.TopicSerializer
    filterset_class = filters.TopicFilter
    permission_classes = [IsAuthenticatedOrReadOnly]
    

class TopicPostListView(generics.ListCreateAPIView):
    serializer_class = serializers.PostSerailizer
    filterset_class = filters.PostFilter
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        topic = get_object_or_404(Topic, pk=self.kwargs['topic_id'])
        posts = Post.objects.filter(topic=topic, content__isnull=False)

        return posts

    # def list(self, request, topic_id, *args, **kwargs):
    #     topic = get_object_or_404(Topic, pk=topic_id)
    #     posts = Post.objects.filter(topic=topic)
    #     serializer = self.get_serializer(posts, many=True)

    #     return Response(serializer.data)
    
    def create(self, request, topic_id, *args, **kwargs):
        topic = get_object_or_404(Topic, pk=topic_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, topic=topic)

        return Response(serializer.data)


class PostListView(generics.ListAPIView):
    queryset = Post.objects.filter(content__isnull=False)
    serializer_class = serializers.PostSerailizer
    filterset_class = filters.PostFilter
    

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.filter(content__isnull=False)
    serializer_class = serializers.PostSerailizer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]
    lookup_field = 'pk'
    lookup_url_kwarg = 'post_id'

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.get_serializer(post)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        post = self.get_object()
        partial = kwargs.get('partial', False)
        serializer = self.get_serializer(post, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PostReplyListView(generics.ListCreateAPIView):
    serializer_class = serializers.ContentSerailizer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'], content__isnull=False)
        replies = Content.objects.filter(reply=post)

        return replies
    
    def create(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, pk=post_id, content__isnull=False)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post, user=request.user)

        return Response(serializer.data)
    

class ReplyListView(generics.ListAPIView):
    queryset = Content.objects.filter(reply__isnull=False)
    serializer_class = serializers.ContentSerailizer

    
class ReplyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Content.objects.filter(reply__isnull=False)
    serializer_class = serializers.ContentSerailizer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]
    lookup_field = 'pk'
    lookup_url_kwarg = 'reply_id'


class ReplyCommentListView(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerailizer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        content = get_object_or_404(Content, pk=self.kwargs['reply_id'])
        comments = Comment.objects.filter(content=content)

        return comments
    
    def create(self, request, *args, **kwargs):
        content = get_object_or_404(Content, pk=self.kwargs['reply_id'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(content=content, user=request.user)

        return Response(serializer.data)
    

class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerailizer


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerailizer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]
    lookup_field = 'pk'
    lookup_url_kwarg = 'comment_id'

