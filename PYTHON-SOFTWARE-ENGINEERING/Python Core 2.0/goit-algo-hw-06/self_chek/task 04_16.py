class Animal:
    color = 'white'  # колір тварини

    def __init__(self, nickname, weight):
        self.nickname = nickname   # Нік тварини
        self.weight = weight   # вага тварини

    def say(self):
        ...
    
    # змінює вагу
    def change_weight(self, new_weight):
        self.weight = new_weight

    # змінює колір
    def change_color(self, new_color):
        Animal.color = new_color

first_animal = Animal('Barsik', 3.9)
second_animal = Animal('Sofiya', 2.8)

first_animal.change_color('red')