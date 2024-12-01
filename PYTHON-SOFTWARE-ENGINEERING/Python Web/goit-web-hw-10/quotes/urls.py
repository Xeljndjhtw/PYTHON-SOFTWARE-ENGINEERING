# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.quotes_list, name='quotes_list'),  # Головна сторінка зі списком цитат
    path('author/<int:pk>/', views.author_detail, name='author_detail'),  # Сторінка автора
    path('add-author/', views.add_author, name='add_author'),  # Додавання автора
    path('add-quote/', views.add_quote, name='add_quote'),  # Додавання цитати
]