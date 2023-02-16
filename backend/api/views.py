from django.shortcuts import render, get_object_or_404
from django.views import View
from rest_framework import generics
from rest_framework.response import Response
from forum.models import Topic, Post, Content
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
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerailizer
    filterset_class = filters.PostFilter
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, topic_id, *args, **kwargs):
        topic = get_object_or_404(Topic, pk=topic_id)
        posts = Post.objects.filter(topic=topic)
        serializer = self.get_serializer(posts, many=True)

        return Response(serializer.data)
    
    def create(self, request, topic_id, *args, **kwargs):
        topic = get_object_or_404(Topic, pk=topic_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, topic=topic)

        return Response(serializer.data)


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerailizer
    filterset_class = filters.PostFilter
    

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
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
        serializer = self.get_serializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
