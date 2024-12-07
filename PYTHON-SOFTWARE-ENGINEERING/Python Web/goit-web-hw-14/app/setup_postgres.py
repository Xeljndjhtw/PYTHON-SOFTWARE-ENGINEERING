#  setup_postgres

import psycopg2
from psycopg2 import sql

# Налаштування для підключення до PostgreSQL (користувач superuser, наприклад, postgres)
DB_SETTINGS = {
    'dbname': 'postgres',      # База за замовчуванням для суперкористувача
    'user': 'postgres',        # Ім'я суперкористувача
    'password': 'admin',       # Пароль суперкористувача
    'host': 'localhost',       # Хост сервера
    'port': '5432',            # Порт за замовчуванням для PostgreSQL
}

# Параметри нової бази даних і користувача
NEW_DB_NAME = "dbbl"            # Ім'я нової бази даних
NEW_USER_NAME = "Xelj"          # Ім'я нового користувача
NEW_USER_PASSWORD = "admin"     # Пароль нового користувача

def setup_database():
    try:
        # Підключення до PostgreSQL
        conn = psycopg2.connect(**DB_SETTINGS)
        conn.autocommit = True  # Автоматичне виконання команд
        cursor = conn.cursor()

        # Створення бази даних
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(NEW_DB_NAME)
        ))
        print(f"База даних '{NEW_DB_NAME}' створена.")

        # Створення нового користувача
        cursor.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s").format(
            sql.Identifier(NEW_USER_NAME)
        ), [NEW_USER_PASSWORD])
        print(f"Користувач '{NEW_USER_NAME}' створений.")

        # Призначення привілеїв користувачеві
        cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
            sql.Identifier(NEW_DB_NAME),
            sql.Identifier(NEW_USER_NAME)
        ))
        print(f"Привілеї для бази даних '{NEW_DB_NAME}' надано користувачу '{NEW_USER_NAME}'.")

    except Exception as e:
        print("Сталася помилка:", e)
    finally:
        if conn:
            cursor.close()
            conn.close()
            print("Підключення до PostgreSQL закрито.")

if __name__ == "__main__":
    setup_database()
