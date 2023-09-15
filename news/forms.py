from django import forms
from .models import Post


class SearchForm(forms.Form):
    title = forms.CharField(
        max_length=100, required=False, label='По названию')
    author = forms.CharField(max_length=100, required=False, label='По автору')
    date = forms.DateField(required=False, label='По дате',
                           widget=forms.DateInput(attrs={'type': 'date'}))


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_type', 'title', 'text', 'categories']
