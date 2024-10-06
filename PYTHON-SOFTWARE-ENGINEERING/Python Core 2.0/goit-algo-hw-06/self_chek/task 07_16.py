class Animal:

    def __init__(self, nickname, weight):
        self.nickname = nickname   # Нік тварини
        self.weight = weight   # вага тварини

    # що каже
    def say(self):
        ...
    
    # змінює вагу
    def change_weight(self, new_weight):
        self.weight = new_weight


# дочерній клас (пес)
class Dog(Animal):
    def __init__(self, nickname, weight, breed, owner):
        super().__init__(nickname, weight)
        self.breed = breed   # порода
        self.owner = owner   # хозяїн

    # що каже
    def say(self):
        return 'Woof'
    
    # хто хозяїн
    def who_is_owner(self):
        return owner.info()
    
# клас 'власник'
class Owner:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def info(self):
        return {'name': owner.name, 'age': owner.age, 'address': owner.address}
         


owner= Owner('Sherlock', 24, 'London, 221B Baker street')
dog = Dog('Barbos', 23, 'labrador', owner.info())

print(owner.info())
# print(owner.__dict__)
print (dog.__dict__)

