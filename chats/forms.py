# messages/forms.py

from django import forms
from django.contrib.auth import get_user_model
from .models import Message

class MessageForm(forms.ModelForm):
    sender = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Sender'
    )

    class Meta:
        model = Message
        fields = ['sender', 'child', 'message_text']
        widgets = {
            'message_text': forms.Textarea(attrs={'class': 'form-control'}),
        }
