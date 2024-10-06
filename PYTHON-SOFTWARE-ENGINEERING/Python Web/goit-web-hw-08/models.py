# models.py
from mongoengine import Document, StringField, ReferenceField, ListField

# Модель для авторів
class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

# Модель для цитат
class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, required=True)
    quote = StringField(required=True)
