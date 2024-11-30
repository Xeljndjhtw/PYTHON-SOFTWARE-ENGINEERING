# producer.py

import pika
import json
from mongoengine import Document, StringField, BooleanField, connect
from faker import Faker

# Підключення до MongoDB
connect(host="mongodb+srv://Xeljndjhtw:05071991Xeljndjhtw@xeljndjhtw.auq5p.mongodb.net/?retryWrites=true&w=majority&appName=Xeljndjhtw")

# Модель для контакту
class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    sent = BooleanField(default=False)

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Створення черги
channel.queue_declare(queue='email_queue')

# Генерація контактів та відправка у чергу
fake = Faker()

def generate_contacts(count):
    for _ in range(count):
        contact = Contact(
            fullname=fake.name(),
            email=fake.email()
        )
        contact.save()
        # Відправка ObjectID контакту у чергу
        channel.basic_publish(
            exchange='',
            routing_key='email_queue',
            body=json.dumps({"contact_id": str(contact.id)})
        )
        print(f"Контакт {contact.fullname} додано до черги.")

if __name__ == "__main__":
    contact_count = int(input("Скільки контактів створити? "))
    generate_contacts(contact_count)
    connection.close()