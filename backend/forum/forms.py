from django import forms
from . import models


class TopicForm(forms.ModelForm):
    class Meta:
        model = models.Topic
        fields = ('name',)


class PostCreateForm(forms.Form):
    title = forms.CharField(max_length=50)
    context = forms.CharField(max_length=5000)


class ReplyCreateForm(forms.ModelForm):
    class Meta:
        model = models.Content
        fields = ('text',)


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('text',)