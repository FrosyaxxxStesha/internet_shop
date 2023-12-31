from django.forms import ModelForm
from .models import Post


class PostModelForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'preview_image')

