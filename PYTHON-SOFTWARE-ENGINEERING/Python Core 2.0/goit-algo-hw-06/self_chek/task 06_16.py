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

    # дочерній клас (кiт)
class Cat(Animal):
    def __init__(self, nickname, weight, breed):
        super().__init__(nickname, weight)
        self.breed = breed   # порода

    # що каже
    def say(self):
        return 'Meow'
    
   # дочерній клас (пес)
class Dog(Animal):
    def __init__(self, nickname, weight, breed):
        super().__init__(nickname, weight)
        self.breed = breed   # порода

    # що каже
    def say(self):
        return 'Woof'



# перевірка роботи коду
cat = Cat('Simon', 10, 'british')
dog = Dog('Barbos', 23, 'labrador')

print(f'cat say {cat.say()}')
print(f'dog say {dog.say()}')

