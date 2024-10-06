import copy
import pickle


class Person:
    def __init__(self, name: str, email: str, phone: str, favorite: bool):
        self.name = name
        self.email = email
        self.phone = phone
        self.favorite = favorite

    def __copy__(self):
        """Реалізація поверхневого копіювання для класу Person."""
        return Person(self.name, self.email, self.phone, self.favorite)


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

    def __copy__(self):
        """Реалізація поверхневого копіювання для класу Contacts."""
        # Використовуємо метод copy для створення поверхневої копії
        copied_contacts = Contacts(self.filename, self.contacts[:])
        copied_contacts.count_save = self.count_save
        copied_contacts.is_unpacking = self.is_unpacking
        return copied_contacts

    def __deepcopy__(self, memo):
        """Реалізація глибокого копіювання для класу Contacts."""
        # Використовуємо метод deepcopy для глибокої копії
        copied_contacts = Contacts(
            copy.deepcopy(self.filename, memo),
            copy.deepcopy(self.contacts, memo)
        )
        copied_contacts.count_save = self.count_save
        copied_contacts.is_unpacking = self.is_unpacking
        return copied_contacts


# Приклад використання
original_person = Person("John Doe", "johndoe@example.com", "1234567890", True)
copied_person = copy.copy(original_person)
print(f"Original: {original_person.name}, Copied: {copied_person.name}")

original_contacts = Contacts("contacts.pkl", [
    Person("John Doe", "johndoe@example.com", "1234567890", True),
    Person("Jane Doe", "janedoe@example.com", "0987654321", False)
])

# Створення поверхневої копії
shallow_copied_contacts = copy.copy(original_contacts)
print(original_contacts.contacts is shallow_copied_contacts.contacts)  # Повинно вивести True

# Створення глибокої копії
deep_copied_contacts = copy.deepcopy(original_contacts)
print(original_contacts.contacts is deep_copied_contacts.contacts)  # Повинно вивести False
