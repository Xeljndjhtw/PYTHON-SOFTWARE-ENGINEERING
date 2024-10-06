import sqlite3
from faker import Faker
import random

# Ініціалізуємо Faker
fake = Faker()

# Підключаємося до бази даних SQL
conn = sqlite3.connect('university.db')
cursor = conn.cursor()

# Створюємо таблиці
cursor.execute('''
    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        group_id INTEGER,
        FOREIGN KEY(group_id) REFERENCES groups(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        teacher_id INTEGER,
        FOREIGN KEY(teacher_id) REFERENCES teachers(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject_id INTEGER,
        grade INTEGER,
        date TEXT,
        FOREIGN KEY(student_id) REFERENCES students(id),
        FOREIGN KEY(subject_id) REFERENCES subjects(id)
    )
''')

conn.commit()

# Створюємо 3 групи
group_ids = []
for _ in range(3):
    cursor.execute("INSERT INTO groups (name) VALUES (?)", (fake.word(),))
    group_ids.append(cursor.lastrowid)

# Створюємо 5 викладачів
teacher_ids = []
for _ in range(5):
    cursor.execute("INSERT INTO teachers (name) VALUES (?)", (fake.name(),))
    teacher_ids.append(cursor.lastrowid)

# Створюємо 8 предметів
subject_ids = []
for _ in range(8):
    teacher_id = random.choice(teacher_ids)
    cursor.execute("INSERT INTO subjects (name, teacher_id) VALUES (?, ?)", (fake.word(), teacher_id))
    subject_ids.append(cursor.lastrowid)

# Створюємо 50 студентів і розподіляємо їх по групах
student_ids = []
for _ in range(50):
    group_id = random.choice(group_ids)
    cursor.execute("INSERT INTO students (name, group_id) VALUES (?, ?)", (fake.name(), group_id))
    student_ids.append(cursor.lastrowid)

# Додаємо 20 оцінок кожному студенту для кожного предмета
for student_id in student_ids:
    for subject_id in subject_ids:
        for _ in range(3):
            grade = random.randint(6, 12)  # Оцінки від 6 до 12
            date = fake.date_this_year().isoformat()
            cursor.execute("INSERT INTO grades (student_id, subject_id, grade, date) VALUES (?, ?, ?, ?)",
                           (student_id, subject_id, grade, date))

conn.commit()

# Збереження SQL-запитів у файли
queries = {
    1: "SELECT students.name, AVG(grades.grade) as average_grade FROM students JOIN grades ON students.id = grades.student_id GROUP BY students.id ORDER BY average_grade DESC LIMIT 5;",
    2: "SELECT students.name, AVG(grades.grade) as average_grade FROM students JOIN grades ON students.id = grades.student_id WHERE grades.subject_id = ? GROUP BY students.id ORDER BY average_grade DESC LIMIT 1;",
    3: "SELECT groups.name, AVG(grades.grade) as average_grade FROM groups JOIN students ON groups.id = students.group_id JOIN grades ON students.id = grades.student_id WHERE grades.subject_id = ? GROUP BY groups.id;",
    4: "SELECT AVG(grade) as average_grade FROM grades;",
    5: "SELECT subjects.name FROM subjects WHERE subjects.teacher_id = ?;",
    6: "SELECT students.name FROM students WHERE students.group_id = ?;",
    7: "SELECT students.name, grades.grade FROM students JOIN grades ON students.id = grades.student_id WHERE students.group_id = ? AND grades.subject_id = ?;",
    8: "SELECT AVG(grades.grade) as average_grade FROM grades JOIN subjects ON grades.subject_id = subjects.id WHERE subjects.teacher_id = ?;",
    9: "SELECT subjects.name FROM subjects JOIN grades ON subjects.id = grades.subject_id WHERE grades.student_id = ?;",
    10: "SELECT subjects.name FROM subjects JOIN grades ON subjects.id = grades.subject_id WHERE grades.student_id = ? AND subjects.teacher_id = ?;"
}

for query_num, query in queries.items():
    with open(f"query_{query_num}.sql", "w") as file:
        file.write(query)
