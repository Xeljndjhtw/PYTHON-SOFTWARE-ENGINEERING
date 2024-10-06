import json


def write_contacts_to_file(filename, contacts):
    with open(filename, 'w') as f:
        json.dump({'contacts': contacts}, f, indent=4)
    
        


def read_contacts_from_file(filename):
    with open(filename, 'r') as f:
        unload = json.load(f)
        return unload.get('contacts')
