from sqlalchemy import func, desc
from models import Student, Grade, Subject, Teacher, Group
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:mysecretpassword@localhost:5432/my_database')
Session = sessionmaker(bind=engine)
session = Session()

# Приклад запитів
def select_1():
    # Знайти 5 студентів із найбільшим середнім балом з усіх предметів
    return session.query(
        Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')
    ).join(Grade).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()



