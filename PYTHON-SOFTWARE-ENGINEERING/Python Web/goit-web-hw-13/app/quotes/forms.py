# forms.py

from django import forms
from .models import Author, Quote

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'bio']    # Поля форми для автора

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'author'] # Поля форми для цитати