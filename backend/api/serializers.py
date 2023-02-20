from rest_framework import serializers
from forum.models import Topic, Post, Content, Comment
from django.contrib.auth import get_user_model


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username']
        read_only_fields = ['id', 'username']


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name']


class ContentSerailizer(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)
    class Meta:
        model = Content
        fields = ['id', 'text', 'user']


    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()

        return instance
    
    def create(self, validated_data):
        post = validated_data.pop('post')
        user = validated_data.pop('user')
        content = Content.objects.create(user=user, reply=post, **validated_data)

        return content


class PostSerailizer(serializers.ModelSerializer):
    topic = TopicSerializer(read_only=True)
    content = ContentSerailizer()
    user = UserSerializers(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'topic', 'title', 'content']
        read_only_fields = ['id', 'user', 'topic']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        content_data = validated_data.get('content', {})
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
        Content.objects.create(post=post, user=user, **content_data)

        return post


class CommentSerailizer(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text']

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.save()

        return instance
    
    def create(self, validated_data):
        content = validated_data.pop('content')
        user = validated_data.pop('user')
        comment = Comment.objects.create(content=content, user=user, **validated_data)

        return comment
    