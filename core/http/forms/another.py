"""
Project base forms
"""
from django import forms
from django_ckeditor_5 import widgets

from core.http import models


class PostAdminForm(forms.ModelForm):
    class Meta:
        model = models.Post
        widgets = {
            'desc': widgets.CKEditor5Widget(),
        }
        fields = '__all__'
