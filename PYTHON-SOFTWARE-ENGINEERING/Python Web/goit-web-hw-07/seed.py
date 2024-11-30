from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Group, Student, Teacher, Subject, Grade
import random
from datetime import datetime

# Налаштування підключення до бази даних
engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/my_database')
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

def seed_data():
    # Створення груп
    groups = [Group(name=f"Group {i}") for i in range(1, 4)]
    session.add_all(groups)
    session.commit()
    
    # Створення викладачів
    teachers = [Teacher(fullname=fake.name()) for _ in range(3)]
    session.add_all(teachers)
    session.commit()
    
    # Створення предметів
    subjects = [Subject(name=f"Subject {i}", teacher=random.choice(teachers)) for i in range(1, 6)]
    session.add_all(subjects)
    session.commit()

    # Створення студентів
    students = [Student(fullname=fake.name(), group=random.choice(groups)) for _ in range(30)]
    session.add_all(students)
    session.commit()

    # Створення оцінок
    for student in students:
        for subject in subjects:
            for _ in range(20):  # Додаємо 20 оцінок для кожного студента по кожному предмету
                grade = Grade(
                    student=student,
                    subject=subject,
                    grade=random.uniform(60, 100),
                    date=fake.date_this_year()
                )
                session.add(grade)
    session.commit()

if __name__ == "__main__":
    seed_data()
    print("Database seeded successfully.")
