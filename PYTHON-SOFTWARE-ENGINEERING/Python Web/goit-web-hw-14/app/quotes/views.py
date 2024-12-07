from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Author, Quote
from .forms import AuthorForm, QuoteForm

# Відображення всіх цитат
def quotes_list(request):
    quotes = Quote.objects.all()
    return render(request, 'quotes/quotes_list.html', {'quotes': quotes})

# Відображення інформації про автора
def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, 'quotes/author_detail.html', {'author': author})

# Додавання нового автора (тільки для авторизованих юзерів)
@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes_list')
    else:
        form = AuthorForm()
    return render(request, 'quotes/add_author.html', {'form': form})

# Додавання нової цитати (тільки для авторизованих юзерів)
@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes_list')
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})