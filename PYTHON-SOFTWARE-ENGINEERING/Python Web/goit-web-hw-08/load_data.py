# load_data.py
import json
from mongoengine import connect
from models import Author, Quote  # Імпортуємо моделі з models.py

# Підключення до бази даних MongoDB Atlas
connect(host='YOUR_MONGODB_ATLAS_CONNECTION_STRING')

# Завантаження даних авторів з файлу authors.json
def load_authors():
    with open('authors.json', 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author in authors_data:
            new_author = Author(
                fullname=author['fullname'],
                born_date=author.get('born_date'),
                born_location=author.get('born_location'),
                description=author.get('description')
            )
            new_author.save()
        print("Дані авторів успішно завантажені.")

# Завантаження даних цитат з файлу quotes.json
def load_quotes():
    with open('quotes.json', 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote in quotes_data:
            author = Author.objects(fullname=quote['author']).first()
            if author:
                new_quote = Quote(
                    tags=quote['tags'],
                    author=author,
                    quote=quote['quote']
                )
                new_quote.save()
        print("Дані цитат успішно завантажені.")

if __name__ == "__main__":
    load_authors()
    load_quotes()
