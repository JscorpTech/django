#####################
# Project base forms
#####################
from django import forms
from django_ckeditor_5 import widgets

from core.http.models import Post


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        widgets = {
            'desc': widgets.CKEditor5Widget(),
        }
        fields = '__all__'
