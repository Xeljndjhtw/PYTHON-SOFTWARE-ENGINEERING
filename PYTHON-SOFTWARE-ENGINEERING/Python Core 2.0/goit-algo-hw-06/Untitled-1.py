class Field:
    """Базовий клас для полів запису."""
    pass


class Name(Field):
    """Клас для зберігання імені контакту. Обов'язкове поле."""
    
    def __init__(self, name: str):
        self.name = name


class Phone(Field):
    """Клас для зберігання номера телефону. Має валідацію формату (10 цифр)."""
    
    def __init__(self, phone: str):
        self.phone = phone
        self.validate_phone()

    def validate_phone(self):
        if not (self.phone.isdigit() and len(self.phone) == 10):
            raise ValueError("Телефон повинен містити 10 цифр.")


class Record:
    """Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів."""
    
    def __init__(self, name: Name, phones=None):
        self.name = name
        self.phones = phones if phones is not None else []

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def remove_phone(self, phone: Phone):
        self.phones = [p for p in self.phones if p.phone != phone.phone]

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        for i, p in enumerate(self.phones):
            if p.phone == old_phone.phone:
                self.phones[i] = new_phone

    def find_phone(self, phone: str) -> bool:
        return any(p.phone == phone for p in self.phones)


class AddressBook:
    """Клас для зберігання та управління записами."""
    
    def __init__(self):
        self.records = {}

    def add_record(self, record: Record):
        self.records[record.name.name] = record

    def find_record(self, name: str) -> Record:
        return self.records.get(name)

    def remove_record(self, name: str):
        if name in self.records:
            del self.records[name]


# Приклад використання:
address_book = AddressBook()

# Додавання запису
name = Name("Іван")
phone1 = Phone("1234567890")
phone2 = Phone("0987654321")

record = Record(name)
record.add_phone(phone1)
record.add_phone(phone2)

address_book.add_record(record)

# Пошук запису
found_record = address_book.find_record("Іван")
if found_record:
    print(f"Знайдено запис для {found_record.name.name}")

# Видалення запису
address_book.remove_record("Іван")
