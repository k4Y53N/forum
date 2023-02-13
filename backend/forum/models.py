from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Post(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def preview(self):
        return self.content.text[0:100]


class Tag(models.Model):
    name = models.CharField(max_length=20)
    posts = models.ManyToManyField(Post)


class Content(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    post = models.OneToOneField(Post, on_delete=models.SET_NULL, null=True)
    reply = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, related_name='replies')
    text = models.CharField(max_length=5000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def is_context(self):
        return self.post != None


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    content = models.ForeignKey(Content, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=3000, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
