from django import forms
from .models import Suggestion

class SuggestionForm(forms.ModelForm):
	class Meta:
		model = Suggestion
		fields = ['name', 'body']
    # name = forms.CharField(label='name', max_length=100)
    # body = forms.CharField(label='body', max_length=100)