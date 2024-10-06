from collections import UserDict


class Field:
    """Базовий клас для полів запису."""
    pass


class Name(Field):
    """Клас для зберігання імені контакту. Обов'язкове поле."""

    def __init__(self, value: str):
        self.value = value


class Phone(Field):
    """Клас для зберігання номера телефону. Має валідацію формату (10 цифр)."""

    def __init__(self, value: str):
        self.value = value
        self.validate_phone()

    def validate_phone(self):
        if not (self.value.isdigit() and len(self.value) == 10):
            raise ValueError("Телефон повинен містити 10 цифр.")


class Record:
    """Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів."""

    def __init__(self, name: Name, phones=None):
        self.name = name
        self.phones = phones if phones is not None else []

    def add_phone(self, phone: str):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone: str):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone: str, new_phone: str):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError("Старий номер телефону не знайдено.")

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None


class AddressBook(UserDict):
    """Клас для зберігання та управління записами."""

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def __str__(self):
        return "\n".join(
            f"Name: {record.name.value}, Phones: {[phone.value for phone in record.phones]}"
            for record in self.data.values()
        )


# Приклад використання:
address_book = AddressBook()

# Додавання запису
name = Name("John")
phone1 = "1234567890"
phone2 = "5555555555"

record = Record(name)
record.add_phone(phone1)
record.add_phone(phone2)

address_book.add_record(record)



# Пошук запису
found_record = address_book.find("John")
if found_record:
    print(f"Знайдено запис для {found_record.name.value}")

# Видалення запису
address_book.delete("John")

# Виведення адресної книги
print(address_book)
