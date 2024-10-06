import copy
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


def copy_class_contacts(contacts: Contacts) -> Contacts:
    return copy.deepcopy(contacts)


# Приклад використання
original_contacts = Contacts("contacts.pkl", [
    Person("John Doe", "johndoe@example.com", "1234567890", True),
    Person("Jane Doe", "janedoe@example.com", "0987654321", False)
])

# Створення глибокої копії об'єкта Contacts
copied_contacts = copy_class_contacts(original_contacts)

# Перевірка, що оригінал і копія не є тим самим об'єктом
print(original_contacts is copied_contacts)  # Повинно вивести False

# Перевірка, що копія має ті самі атрибути, але є незалежною копією
print(original_contacts.contacts is copied_contacts.contacts)  # Повинно вивести False

# Перевірка, що вкладені об'єкти також скопійовані
print(original_contacts.contacts[0] is copied_contacts.contacts[0])  # Повинно вивести False
print(copied_contacts.contacts[0].name)  # Повинно вивести "John Doe"
