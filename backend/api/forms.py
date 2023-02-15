from django import forms
from forum import models

class TopicQueryForm(forms.ModelForm):
    class Meta:
        model = models.Topic
        fields = ['name']