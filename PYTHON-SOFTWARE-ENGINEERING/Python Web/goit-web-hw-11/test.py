from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:admin@localhost/contacts_db"
engine = create_engine(DATABASE_URL)

try:
    connection = engine.connect()
    print("Успішно підключено до бази даних!")
    connection.close()
except Exception as e:
    print(f"Помилка підключення: {e}")
