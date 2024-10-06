from collections import UserString


class NumberString(UserString):
    def number_count(self):
        
        counter = 0
        for i in range(10):
            counter += self.count(str(i))

        return counter
    
list = ['скільки 1 цифр 2 у 3 рядку 4']    
counter = NumberString(list)
# counter.number_count()
print(counter.number_count())

