class Animal:

    def __init__(self, nickname, weight):
        self.nickname = nickname   # Нік тварини
        self.weight = weight   # вага тварини

    def say(self):
        ...
    
    # змінює вагу
    def change_weight(self, new_weight):
        self.weight = new_weight

class Cat(Animal):
    def say(self):
        return 'Meow'


# перевірка роботи коду
cat = Cat('Simon', 10)
print(cat.say())

