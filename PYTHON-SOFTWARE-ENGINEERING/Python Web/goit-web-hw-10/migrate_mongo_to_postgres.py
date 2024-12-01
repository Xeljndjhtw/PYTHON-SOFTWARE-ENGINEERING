# migrate_mongo_to_postgres.py

from pymongo import MongoClient
from quotes.models import Author, Quote

mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['Xeljndjhtwb']

authors = mongo_db['authors']
quotes = mongo_db['quotes']

# Міграція авторів
for author in authors.find():
    new_author = Author(name=author['name'], bio=author.get('bio', ''))
    new_author.save()

# Міграція цитат
for quote in quotes.find():
    author = Author.objects.get(name=quote['author'])
    new_quote = Quote(text=quote['text'], author=author)
    new_quote.save()