from django.shortcuts import render, get_object_or_404
from django.views import View
from rest_framework import generics
from rest_framework.response import Response
from forum.models import Topic, Post, Content
from django.http import JsonResponse
from . import filters
from . import serializers


# Create your views here.

# class TopicListCreateView(generics.ListCreateAPIView):
#     def list(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)
    
#     def create(self, request, *args, **kwargs):
#         return super().create(request, *args, **kwargs)
    
#     def get_queryset(self):
#         return super().get_queryset()

class TestView(View):
    def get(self, request):
        filter = filters.TopicFilter(request, request.GET)
        return JsonResponse(filter.data, safe=False)
    

class TopicListView(generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = serializers.TopicSerializer
    filterset_class = filters.TopicFilter
    

class TopicPostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerailizer

    def list(self, request, topic_id, *args, **kwargs):
        topic = get_object_or_404(Topic, pk=topic_id)
        posts = Post.objects.filter(topic=topic)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
    
    def create(self, request, topic_id, *args, **kwargs):
        topic = get_object_or_404(Topic, pk=topic_id)
        serializer = serializers.PostSerailizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.data['title']
        context = serializer.data['content']['text']
        post = Post.objects.create(topic=topic, user=request.user, title=title)
        Content.objects.create(post=post, text=context, user=request.user)
        serializer = self.get_serializer(post)

        return Response(serializer.data)


class PostDetailView(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerailizer
    lookup_field = 'pk'
    lookup_url_kwarg = 'post_id'

    def retrieve(self, request, post_id, *args, **kwargs):
        post = self.get_object()
        serializer = self.get_serializer(post)
        return Response(serializer.data)
