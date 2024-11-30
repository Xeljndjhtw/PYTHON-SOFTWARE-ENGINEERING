class Contacts:
    current_id = 1

    def __init__(self):
        
        # Ініціадізація порожнього списку для зберігяння контактів
        self.contacts = []

    def list_contacts(self):
        # Повертає спикок контактів
        return self.contacts

    def add_contacts(self, name, phone, email, favorite):
        #  Створює новий контакт у типі словника
        contact = {
                'id': Contacts.current_id,  # Використовує змінну класу current_id
                'name': name,
                'phone': phone,
                'email': email,
                'favorite': favorite
        }
        # Додає контакт до списку contacts
        self.contacts.append(contact)
        
        # Збільщує cyrrent_id для наступного контакту
        Contacts.current_id += 1