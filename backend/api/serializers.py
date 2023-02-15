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
    replies = ContentSerailizer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'topic' ,'title', 'content', 'replies']
        read_only_fields = ['topic', 'replies']

    def update(self, instance, validated_data):
        title = validated_data['title']
        context = validated_data['content']['text']
        instance.title = title
        instance.content.text = context
        instance.content.save()
        instance.save()

        return instance

