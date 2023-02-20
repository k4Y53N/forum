import json
import os
import random

import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils.lorem_ipsum import paragraphs, words
from forum.models import *



# exec(open('shell.py', 'r').read())

# from django.core.management.utils import get_random_secret_key
# print(get_random_secret_key())

# from rest_framework.settings import api_settings
# print(api_settings.DEFAULT_PAGINATION_CLASS)


def delete_all():
    get_user_model().objects.all().delete()

    Topic.objects.all().delete()
    Post.objects.all().delete()
    Content.objects.all().delete()
    Comment.objects.all().delete()


def create_user():
    user = get_user_model().objects.create_user(
        username='admin', email='admin@email.com', is_superuser=True, password='dev1234')
    with open('random_user.json', 'r') as f:
        users = json.load(f)

    random_usernames = random.sample(users, k=5)

    for username in random_usernames:
        user = get_user_model().objects.create_user(
            username=username,
            email=f'{username}@email.com',
            password=f'{username}123'
        )


def create_topic():
    topics = ['python', 'java', 'c#', 'c++', 'sql', 'mysql',
              'psql', 'mssql', 'socket', 'clean code', 'data structure']
    topic_objs = [Topic(name=topic) for topic in topics]
    Topic.objects.bulk_create(topic_objs)


def create_post():
    users = get_user_model().objects.all()

    def posts_iter():
        for topic in Topic.objects.all():
            r = random.choice(range(5, 21))
            for i in range(1, r):
                user = random.choice(users)
                yield Post(
                    topic=topic,
                    user=user,
                    title=f'{topic.name}\'s post {i}'
                )

    Post.objects.bulk_create(posts_iter())
    posts = Post.objects.all()

    def contents_iter():
        for post in posts:
            para = '\n'.join(paragraphs(random.randint(1, 6)))
            yield Content(
                post=post,
                user=post.user,
                text=f"###{post.title}'s context\n{para}"
            )

    Content.objects.bulk_create(contents_iter())


def create_reply():
    posts = Post.objects.all()
    users = get_user_model().objects.all()

    def content_iter():
        for post in posts:
            r = random.randint(1, 4)
            for _ in range(1, r):
                user = random.choice(users)
                yield Content(
                    user=user,
                    reply=post,
                    text='\n'.join(paragraphs(random.randint(1, 3))
                                   )
                )
    Content.objects.bulk_create(content_iter())


def create_comment():
    contents = Content.objects.all()
    users = get_user_model().objects.all()
    def comment_iter():
        for content in contents:
            r = random.randint(0, 4)
            for i in range(r):
                user = random.choice(users)
                yield Comment(
                    content=content,
                    user=user, 
                    text=words(random.randint(5, 25 + 1))
                )

    Comment.objects.bulk_create(comment_iter())



# delete_all()
# create_user()
# create_topic()
# create_post()
# create_reply()
create_comment()
