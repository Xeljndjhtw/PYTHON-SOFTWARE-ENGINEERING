class IDException(Exception):
    def __init__(self, message='Код не починається з 01'):
        self.message = message
        super().__init__(self.message)

def add_id(id_list, employee_id):
    if employee_id[:2] == '01':
        id_list.append(employee_id)
        return id_list
    else:
        raise IDException()