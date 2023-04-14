from django.db import models
from django.db.models import F, Count
from django.contrib.auth import get_user_model
# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'topic'
        ordering = ['-updated']
        indexes = [
            models.Index(fields=['name'], name='name_idx')
        ]

    def __str__(self) -> str:
        return self.name

class Post(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post'
        ordering = ['-created']
        indexes = [
            models.Index(fields=['title'], name='title_idx')
        ]

    def __str__(self) -> str:
        return f'[{self.user.username}]{self.title}'

    @property
    def preview(self):
        return self.content.text[0:100]


class Tag(models.Model):
    name = models.CharField(max_length=20)
    posts = models.ManyToManyField(Post)

    class Meta:
        db_table = 'tag'

    def __str__(self) -> str:
        return self.name


class Content(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    post = models.OneToOneField(Post, on_delete=models.SET_NULL, null=True)
    reply = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, related_name='replies')
    text = models.CharField(max_length=5000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content'

    def __str__(self) -> str:
        return self.text[:20]

    def is_context(self):
        return self.post != None


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    content = models.ForeignKey(Content, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=3000, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comment'
        ordering = ['created']

    def __str__(self) -> str:
        return f'[{self.user.username}]{self.text[:20]}'