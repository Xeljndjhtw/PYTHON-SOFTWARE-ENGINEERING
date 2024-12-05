from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)     # Ім'я автора
    bio = models.TextField()    # Біографія автора

    def __str__(self):
        return self.name

class Quote(models.Model):
    text = models.TextField()   # Текст цитати
    author = models.ForeignKey(Author, on_delete=models.CASCADE)    # Автор цитати

    def __str__(self):
        return self.text[:50]