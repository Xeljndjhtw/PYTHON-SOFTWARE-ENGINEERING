from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # клас зберегання імені контакту
	def __init__(self, name: str):
          self.name = name


class Phone(Field):
    #  клас зберігає номер телефону
    def __init__(self, phone: str):
         self.phone = phone
         self.validate_phone()

    def validate_phone(self):
         if not (self.phone.isdigit() and len(self.phone) == 10):
              raise ValueError('Номер телефону має містити 10 цифр.')

	
class Record:
    # клас для зберігання інформації про контакт
    def __init__(self, name: Name, phones=None):
        self.name = Name(name)
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
    
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.phone for p in self.phones)}"


class AddressBook(UserDict):
    # клас для зберешання та керування запимсами
    def __init__(self):
        self.records = {}
        super().__init__()
          
    def add_record(self, record: Record):
        self.records[record.name.name] = record

    def find_record(self, name: str) -> Record:
         return self.records.get(name)
    
    def remove_record(self,name: str):
         if name in self.records:
              del self.records[name]



# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
     
print(book)

# Знаходження та редагування телефону для John
john = book.find_record("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

# Видалення запису Jane
book.remove_record("Jane")