import socket
import json
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import threading

# Ініціалізуємо Flask додаток
app = Flask(__name__)

# Шлях до файлу, де зберігатимуться дані
data_file_path = os.path.join("storage", "data.json")

# Створюємо директорію storage, якщо вона не існує
if not os.path.exists("storage"):
    os.makedirs("storage")

# Функція для збереження даних у файл JSON
def save_to_json(data):
    if os.path.exists(data_file_path):
        with open(data_file_path, "r") as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = {}
    else:
        existing_data = {}

    # Додаємо новий запис з часовою міткою
    timestamp = datetime.now().isoformat()
    existing_data[timestamp] = data

    # Записуємо оновлені дані у файл
    with open(data_file_path, "w") as file:
        json.dump(existing_data, file, indent=2)

# Маршрут для головної сторінки
@app.route('/')
def index():
    return render_template('index.html')

# Маршрут для сторінки з формою
@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message_content = request.form.get('message')

        data_to_send = {
            "username": name,
            "message": message_content
        }

        # Пересилання даних через UDP Socket
        udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_client.sendto(str(data_to_send).encode('utf-8'), ('localhost', 5000))
        udp_client.close()

        return redirect(url_for('index'))
    return render_template('message.html')

# Обробка помилки 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

# Функція для запуску UDP-сокет-сервера
def start_udp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 5000))

    print("UDP-сервер запущений і чекає на повідомлення...")

    while True:
        message, _ = server_socket.recvfrom(1024)  # Приймаємо до 1024 байт
        try:
            # Перетворюємо отримані байти у словник
            data = eval(message.decode('utf-8'))
            save_to_json(data)
            print(f"Отримано та збережено повідомлення: {data}")
        except Exception as e:
            print(f"Помилка при обробці повідомлення: {e}")

# Функція для запуску Flask-сервера
def start_flask_server():
    app.run(port=3000, debug=True)

if __name__ == '__main__':
    # Запуск UDP-сервера у новому потоці
    udp_thread = threading.Thread(target=start_udp_server)
    udp_thread.daemon = True
    udp_thread.start()

    # Запуск Flask-сервера у головному потоці
    start_flask_server()
