class Animal:
    def __init__(self, nickname, weight):
        self.nickname = nickname   # Нік тварини
        self.weight = weight   # вага тварини

    def say(self):
        ...
    
    def change_weight(self, weight):
        self.weight = weight

animal = Animal('Barsik', f'{3.9}kg')
animal.change_weight(12)

print(animal.__dict__)