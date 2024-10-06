class Animal:
    def __init__(self, nickname, weight):
        self.nickname = nickname   # Нік тварини
        self.weight = weight   # вага тварини

    def say(self):
        ...

animal = Animal('Barsik', f'{3.9}kg')

# print(animal.__dict__)