import pickle


class Person:
    def __init__(self, name: str, email: str, phone: str, favorite: bool):
        self.name = name
        self.email = email
        self.phone = phone
        self.favorite = favorite


class Contacts:
    def __init__(self, filename: str, contacts: list[Person] = None):
        self.filename = filename
        self.contacts = contacts
        self.count_save = 0
        if contacts is None:
            self.contacts = []
        
    def save_to_file(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self, file)

        
    def read_from_file(self):
        with open(self.filename, 'rb') as file:
            unpacked = pickle.load(file)
            return unpacked 
        

    def __getstate__(self):
        attributes = self.__dict__.copy()
        attributes['count_save'] += 1
        return attributes

        
            
        