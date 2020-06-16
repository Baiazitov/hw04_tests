from django import forms
from .models import  Post
from django.db import models

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ["group", "text"]
        labels = {"group": "Группа", "text": "Текст поста"}
        help_texts = {"text": "Введите текст"}
