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

# дочерній клас (кіт)
class Cat(Animal):
    # що каже
    def say(self):
        return 'Meow'


class CatDog:

    def __init__(self, nickname, weight):
        self.nickname = nickname
        self.weight = weight

    # що каже
    def say(self):
        return 'Meow'
    
    # змінює вагу
    def change_weight(self, new_weight):
        self.weight = new_weight
    

# Використання
catdog = CatDog()
catdog.say()
