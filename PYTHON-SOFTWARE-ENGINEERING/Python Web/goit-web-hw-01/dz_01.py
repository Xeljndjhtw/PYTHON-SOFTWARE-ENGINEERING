from abc import ABC, abstractmethod
import pickle
from collections import UserDict
from datetime import datetime, timedelta

# Абстрактний базовий клас для уявлень
class BaseView(ABC):

    @abstractmethod
    def show_contacts(self, contacts):
        pass

    @abstractmethod
    def show_commands(self, commands):
        pass

# Конкретний клас для відображення інформації через консоль
class ConsoleView(BaseView):

    def show_contacts(self, contacts):
        if not contacts:
            print("No contacts found.")
        for name, record in contacts.items():
            phones = ', '.join(phone.value for phone in record.phones)
            birthday = record.show_birthday()
            print(f"Name: {name}, Phones: {phones}, Birthday: {birthday}")

    def show_commands(self, commands):
        print("Available commands:")
        for command, description in commands.items():
            print(f"{command}: {description}")

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

class Birthday(Field):
    """Клас для зберігання та валідації дня народження."""

    def __init__(self, value: str):
        self.value = value
        self.validate_birthday()

    def validate_birthday(self):
        try:
            datetime.strptime(self.value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Дата народження має бути в форматі DD.MM.YYYY")

class Record:
    """Клас для зберігання інформації про контакт, включаючи ім'я, список телефонів та день народження."""

    def __init__(self, name: Name, phones=None, birthday=None):
        self.name = name
        self.phones = phones if phones is not None else []
        self.birthday = birthday

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

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        return self.birthday.value if self.birthday else "День народження не встановлено."

class AddressBook(UserDict):
    """Клас для зберігання та управління записами."""

    def __init__(self, view: BaseView):
        super().__init__()
        self.view = view

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Запис з ім'ям {name} не знайдено.")

    def find_partial(self, partial_name: str):
        """Знайти записи, які містять часткове співпадіння з ім'ям."""
        return [record for name, record in self.data.items() if partial_name.lower() in name.lower()]

    def get_upcoming_birthdays(self):
        """Знайти контакти, у яких день народження припадає вперед на 7 днів включно."""
        today = datetime.now().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday = datetime.strptime(record.birthday.value, '%d.%m.%Y').date()
                this_year_birthday = birthday.replace(year=today.year)
                days_until_birthday = (this_year_birthday - today).days

                if 0 <= days_until_birthday <= 7:
                    next_birthday_date = this_year_birthday

                    # Перевірка, чи не випадає день народження на вихідний
                    if next_birthday_date.weekday() >= 5:  # 5 і 6 - це субота і неділя
                        next_birthday_date += timedelta(days=(7 - next_birthday_date.weekday()))

                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "birthday": next_birthday_date.strftime('%d.%m.%Y')
                    })

        return upcoming_birthdays

    def __str__(self):
        return "\n".join(
            f"Name: {record.name.value}, Phones: {[phone.value for phone in record.phones]}, Birthday: {record.show_birthday()}"
            for record in self.data.values()
        )

    def save_to_file(self, file_name: str):
        """Зберегти адресу книгу у файл."""
        with open(file_name, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, file_name: str):
        """Завантажити адресу книгу з файлу."""
        try:
            with open(file_name, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            print("Файл не знайдено, починаємо з порожньої адресної книги.")

# Функції-обробники команд

def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    if record is None:
        record = Record(Name(name))
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Contact updated."
    
    record.add_phone(phone)
    return message

def change_contact(args, book):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    
    try:
        record.edit_phone(old_phone, new_phone)
        return "Phone number changed."
    except ValueError as e:
        return str(e)

def show_phones(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    
    phones = ", ".join(phone.value for phone in record.phones)
    return f"Phones for {name}: {phones}"

def show_all(args, book):
    book.view.show_contacts(book.data)
    return "All contacts shown."

def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    
    try:
        record.add_birthday(birthday)
        return "Birthday added."
    except ValueError as e:
        return str(e)

def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    
    return f"Birthday for {name}: {record.show_birthday()}"

def upcoming_birthdays(args, book):
    birthdays = book.get_upcoming_birthdays()
    if not birthdays:
        return "No upcoming birthdays in the next 7 days."

    result = []
    for bday in birthdays:
        result.append(f"{bday['name']} - {bday['birthday']}")
    return "\n".join(result)

def hello(args, book):
    return "Hello! How can I assist you today?"

def exit_program(args, book, file_name):
    book.save_to_file(file_name)
    return "Goodbye!"

# Декоратор для обробки помилок вводу

def input_error(func):
    def wrapper(args, book, file_name="address_book.pkl"):
        try:
            return func(args, book, file_name)
        except (IndexError, ValueError) as e:
            return f"Error: {str(e)}"
    return wrapper

# Команди та їх обробники

COMMANDS = {
    "add": input_error(add_contact),
    "change": input_error(change_contact),
    "phone": input_error(show_phones),
    "all": input_error(show_all),
    "add-birthday": input_error(add_birthday),
    "show-birthday": input_error(show_birthday),
    "birthdays": input_error(upcoming_birthdays),
    "hello": input_error(hello),
    "exit": input_error(exit_program),
    "close": input_error(exit_program),
}

def main():
    view = ConsoleView()
    book = AddressBook(view)
    file_name = "address_book.pkl"
    book.load_from_file(file_name)

    print("Welcome to your personal assistant bot!")

    while True:
        command_line = input("Enter a command: ")
        parts = command_line.split()
        if not parts:
            continue

        command = parts[0].lower()
        args = parts[1:]

        if command in COMMANDS:
            result = COMMANDS[command](args, book, file_name)
            print(result)

            if command in ("exit", "close"):
                break
        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()
