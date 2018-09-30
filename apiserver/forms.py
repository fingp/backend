from django import forms
from .models import CommentTb

class CommentForm(forms.ModelForm):
    class Meta :
        model = CommentTb
        fields = ('class_code','author_id','content')
