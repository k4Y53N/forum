import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()
from forum.models import *
from django.contrib.auth import get_user_model

# exec(open('shell.py', 'r').read())

user = get_user_model().objects.first()
Topic.objects.all().delete()
Post.objects.all().delete()
Content.objects.all().delete()
Comment.objects.all().delete()
topic = Topic.objects.create(name='python')
post = Post.objects.create(topic=topic, user=user)
content = Content.objects.create(user=user, post=post, text=f'{post.id}\'s context')
reply = Content.objects.create(reply=post, user=user, text=f'{post.id}\'s reply')

for content in Content.objects.all():
    comment = Comment(content=content, text=f'{content.id}\'s comment', user=user)
    comment.save()