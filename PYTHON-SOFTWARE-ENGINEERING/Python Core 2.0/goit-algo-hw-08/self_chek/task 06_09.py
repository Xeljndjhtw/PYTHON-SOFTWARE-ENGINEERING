import pickle


class Person:
    def __init__(self, name: str, email: str, phone: str, favorite: bool):
        self.name = name
        self.email = email
        self.phone = phone
        self.favorite = favorite


class Contacts:
    def __init__(self, filename: str, contacts: list[Person] = None):
        if contacts is None:
            contacts = []
        self.filename = filename
        self.contacts = contacts
        self.count_save = 0
        self.is_unpacking = False  # Атрибут за замовчуванням False

    def save_to_file(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self, file)

    def read_from_file(self):
        with open(self.filename, "rb") as file:
            content = pickle.load(file)
        return content

    def __getstate__(self):
        attributes = self.__dict__.copy()
        attributes["count_save"] += 1
        return attributes

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.is_unpacking = True  # Встановлюємо is_unpacking у True


# Приклад використання
contacts = Contacts("contacts.pkl", [
    Person("John Doe", "johndoe@example.com", "1234567890", True),
    Person("Jane Doe", "janedoe@example.com", "0987654321", False)
])

# Збереження в файл
contacts.save_to_file()

# Завантаження з файлу
loaded_contacts = contacts.read_from_file()

# Перевірка is_unpacking після розпакування
print(f"Is unpacking: {loaded_contacts.is_unpacking}")  # Повинно вивести True
print(f"Count save: {loaded_contacts.count_save}")
for person in loaded_contacts.contacts:
    print(f"Name: {person.name}, Email: {person.email}, Phone: {person.phone}, Favorite: {person.favorite}")
