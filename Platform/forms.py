from django import forms
from .models import Vibe, Revibe


class NewVibeForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'How are you feeling today?'}
        ),
        max_length=4000,
        help_text='The max length of the body is 4000.'
    )

    class Meta:
        model = Vibe
        fields = ['title', 'body']


class NewRevibeForm(forms.ModelForm):
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'Do you share similar vibes?'}
        ),
        max_length=4000,
        help_text='The max length of the body is 4000.'
    )

    class Meta:
        model = Revibe
        fields = ['title', 'body']
