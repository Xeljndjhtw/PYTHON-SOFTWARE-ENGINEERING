from mongoengine import Document, StringField, ReferenceField, ListField, connect
import json

# Підключення до MongoDB Atlas
connect(host="mongodb+srv://Xeljndjhtw:05071991Xeljndjhtw@xeljndjhtw.auq5p.mongodb.net/?retryWrites=true&w=majority&appName=Xeljndjhtw")

# Моделі для збереження даних
class Author(Document):
    fullname = StringField(required=True)  # Повне ім'я автора
    born_date = StringField()  # Дата народження
    born_location = StringField()  # Місце народження
    description = StringField()  # Опис біографії

class Quote(Document):
    tags = ListField(StringField())  # Теги, пов'язані з цитатою
    author = ReferenceField(Author, required=True)  # Посилання на автора
    quote = StringField(required=True)  # Текст цитати

# Функції для завантаження даних у базу даних
def load_authors(file_path):
    """Завантаження авторів із JSON файлу у базу даних."""
    with open(file_path, "r", encoding="utf-8") as file:
        authors = json.load(file)  # Зчитуємо JSON файл
        for author_data in authors:
            author = Author(**author_data)  # Створюємо об'єкт Author
            author.save()  # Зберігаємо автора в базу даних

def load_quotes(file_path):
    """Завантаження цитат із JSON файлу у базу даних."""
    with open(file_path, "r", encoding="utf-8") as file:
        quotes = json.load(file)  # Зчитуємо JSON файл
        for quote_data in quotes:
            author = Author.objects(fullname=quote_data['author']).first()  # Знаходимо автора за ім'ям
            if author:
                quote = Quote(
                    tags=quote_data['tags'],  # Додаємо теги
                    author=author,  # Вказуємо посилання на автора
                    quote=quote_data['quote']  # Додаємо текст цитати
                )
                quote.save()  # Зберігаємо цитату в базу даних

# Функція для пошуку цитат
def search_quotes():
    """Пошук цитат за ім'ям автора, тегом або набором тегів."""
    print("Введіть команду (name:, tag:, tags:, або exit):")
    while True:
        command = input("Command: ").strip()  # Читаємо команду від користувача
        if command.startswith("name:"):
            name = command.split("name:", 1)[1].strip()  # Отримуємо ім'я автора
            authors = Author.objects(fullname__icontains=name)  # Пошук авторів за частковим співпадінням імені
            if authors:
                for author in authors:
                    quotes = Quote.objects(author=author)  # Отримуємо цитати автора
                    for quote in quotes:
                        print(f"{quote.quote} (Tags: {', '.join(quote.tags)})")  # Виводимо цитати
            else:
                print("Цитат для цього автора не знайдено.")
        elif command.startswith("tag:"):
            tag = command.split("tag:", 1)[1].strip()  # Отримуємо тег
            quotes = Quote.objects(tags__icontains=tag)  # Пошук цитат за тегом
            if quotes:
                for quote in quotes:
                    print(f"{quote.quote} (Author: {quote.author.fullname})")  # Виводимо цитати
            else:
                print("Цитат для цього тега не знайдено.")
        elif command.startswith("tags:"):
            tags = command.split("tags:", 1)[1].strip().split(",")  # Отримуємо список тегів
            quotes = Quote.objects(tags__in=tags)  # Пошук цитат за набором тегів
            if quotes:
                for quote in quotes:
                    print(f"{quote.quote} (Author: {quote.author.fullname})")  # Виводимо цитати
            else:
                print("Цитат для цих тегів не знайдено.")
        elif command == "exit":
            print("Вихід...")  # Завершення роботи скрипта
            break
        else:
            print("Невірна команда. Використовуйте name:, tag:, tags:, або exit.")  # Повідомлення про невірну команду

# Завантаження даних у базу даних
if __name__ == "__main__":
    load_authors("authors.json")  # Завантаження авторів
    load_quotes("quotes.json")  # Завантаження цитат
    search_quotes()  # Виконання функції пошуку

