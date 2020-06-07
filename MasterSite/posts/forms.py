from django import forms
from .models import PostModel


class PostForm(forms.ModelForm):
    title = forms.CharField(min_length=4, max_length=50, required=True)
    description = forms.CharField(min_length=30, max_length=500, widget=forms.Textarea, required=True)
    content = forms.CharField(min_length=50, max_length=5000, widget=forms.Textarea, required=True)

    class Meta:
        model = PostModel
        fields = ["title", "image", "description", "content"]
