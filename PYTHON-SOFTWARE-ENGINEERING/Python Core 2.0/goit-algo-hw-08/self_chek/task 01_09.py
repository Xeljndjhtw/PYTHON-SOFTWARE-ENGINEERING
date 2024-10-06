import pickle


def write_contacts_to_file(filename, contacts):
    with open(filename, 'wb') as file:
        pickle.dump(contacts)
    
        


def read_contacts_from_file(filename):
    with open(filename, 'rb') as file:
        unload = pickle.load(file)
        return unload