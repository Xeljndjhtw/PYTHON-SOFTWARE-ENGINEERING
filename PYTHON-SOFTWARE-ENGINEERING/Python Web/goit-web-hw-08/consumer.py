# consumer.py

import pika
import json
from mongoengine import connect
from producer import Contact

# Підключення до MongoDB
connect(host="mongodb+srv://Xeljndjhtw:05071991Xeljndjhtw@xeljndjhtw.auq5p.mongodb.net/?retryWrites=true&w=majority&appName=Xeljndjhtw")

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Створення черги
channel.queue_declare(queue='email_queue')

# Функція для імітації надсилання email
def send_email(contact):
    print(f"Відправка email на {contact.email} ({contact.fullname})...")
    contact.sent = True
    contact.save()
    print(f"Email відправлено {contact.email}.")

# Обробка повідомлення з черги
def callback(ch, method, properties, body):
    data = json.loads(body)
    contact = Contact.objects(id=data["contact_id"]).first()
    if contact and not contact.sent:
        send_email(contact)
    else:
        print(f"Контакт з ID {data['contact_id']} вже оброблений або не знайдений.")

if __name__ == "__main__":
    channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)
    print("Очікування повідомлень. Натисніть CTRL+C для виходу.")
    channel.start_consuming()
