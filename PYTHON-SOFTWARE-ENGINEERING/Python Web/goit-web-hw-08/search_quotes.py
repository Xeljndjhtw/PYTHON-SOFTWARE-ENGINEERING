# search_quotes.py
from mongoengine import connect
from models import Author, Quote  # Імпортуємо моделі з models.py

# Підключення до бази даних MongoDB Atlas
connect(host='YOUR_MONGODB_ATLAS_CONNECTION_STRING')

def search_quotes():
    while True:
        user_input = input("Введіть команду (name, tag, tags, або exit): ").strip()
        
        if user_input.startswith('name:'):
            name = user_input[len('name:'):].strip()
            author = Author.objects(fullname__iexact=name).first()
            if author:
                quotes = Quote.objects(author=author)
                for quote in quotes:
                    print(f"{quote.quote}")
            else:
                print(f"Автор '{name}' не знайдений.")
        
        elif user_input.startswith('tag:'):
            tag = user_input[len('tag:'):].strip()
            quotes = Quote.objects(tags=tag)
            for quote in quotes:
                print(f"{quote.quote}")
        
        elif user_input.startswith('tags:'):
            tags = user_input[len('tags:'):].strip().split(',')
            quotes = Quote.objects(tags__in=tags)
            for quote in quotes:
                print(f"{quote.quote}")
        
        elif user_input.lower() == 'exit':
            print("Завершення програми.")
            break
        
        else:
            print("Невідома команда. Використовуйте name, tag, tags або exit.")

if __name__ == "__main__":
    search_quotes()
