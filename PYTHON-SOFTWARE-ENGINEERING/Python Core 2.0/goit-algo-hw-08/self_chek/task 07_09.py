import copy

class Person:
    def __init__(self, name: str, email: str, phone: str, favorite: bool):
        self.name = name
        self.email = email
        self.phone = phone
        self.favorite = favorite


def copy_class_person(person: Person) -> Person:
    return copy.copy(person)


# Приклад використання
original_person = Person("John Doe", "johndoe@example.com", "1234567890", True)
copied_person = copy_class_person(original_person)

# Перевірка, що оригінал і копія не є тим самим об'єктом
print(original_person is copied_person)  # Повинно вивести False

# Перевірка, що копія має ті самі атрибути
print(copied_person.name)  # Повинно вивести "John Doe"
print(copied_person.email)  # Повинно вивести "johndoe@example.com"
print(copied_person.phone)  # Повинно вивести "1234567890"
print(copied_person.favorite)  # Повинно вивести True
