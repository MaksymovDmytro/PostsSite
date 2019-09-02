from django import forms
from io import BytesIO
from PIL import Image

from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ['author', 'created_timestamp', 'likes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update({'style': 'resize:none; width: 80%'})
        self.fields['title'].widget.attrs.update({'style': 'resize:none; width: 80%'})

    def clean(self):
        image_field = self.cleaned_data.get('post_image')
        if image_field:
            image_file = BytesIO(image_field.read())
            image = Image.open(image_file)
            width, height = image.size

            ratio = 1
            opt_width = 800
            opt_height = 600

            if opt_width / width <= opt_height / height:
                ratio = opt_width / width
            else:
                ratio = opt_height / height

            image = image.resize((int(width * ratio), int(height * ratio)), Image.ANTIALIAS)

            image_file = BytesIO()
            image.save(image_file, 'JPEG', quality=90)

            image_field.file = image_file


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs.update({'class': 'form-control',
                                                    'style': 'resize:none;',
                                                    'rows': 4})
