from rest_framework import serializers
from forum.models import Topic, Post, Content
from django.shortcuts import get_object_or_404


class UserSerializers(serializers.Serializer):
    pass


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name']


class ContentSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['text']


class PostSerailizer(serializers.ModelSerializer):
    topic = TopicSerializer(read_only=True)
    content = ContentSerailizer()
    # replies = ContentSerailizer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'topic', 'title', 'content', 'replies']
        read_only_fields = ['topic', 'replies']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        content_data = validated_data.pop('content')
        content = instance.content
        content.text = content_data.get('text', content.text)
        content.save()
        instance.save()

        return instance

    def create(self, validated_data):
        user = validated_data.pop('user')
        topic = validated_data.pop('topic')
        content_data = validated_data.pop('content')
        post = Post.objects.create(user=user, topic=topic, **validated_data)
        Content.objects.create(post=post, **content_data)

        return post
