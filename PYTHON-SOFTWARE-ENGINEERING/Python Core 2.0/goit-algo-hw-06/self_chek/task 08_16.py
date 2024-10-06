class Animal:

    def __init__(self, nickname, weight):
        self.nickname = nickname   # Нік тварини
        self.weight = weight   # вага тварини

    # що каже
    def say(self):
        ...
    
    def info(self):
        return f'{self.nickname}-{self.weight}'


# дочерній клас (кіт)
class Cat(Animal):
    # що каже
    def say(self):
        return 'Meow'


class Dog(Animal):
    # що каже
    def say(self):
        return 'Woof'
    

class CatDog(Cat, Dog):
    def say(self):
        return super().say()
    
class DogCat(Dog, Cat):
    def say(self):
        return super().say()
    
cat_dog = CatDog('Catty', 5)
dog_cat = DogCat('Doggy', 10)
    

print (cat_dog.info())

