from django.forms import ModelForm
from .models import Post


class PostModelForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'preview_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'