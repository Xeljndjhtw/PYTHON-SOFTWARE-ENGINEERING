import random

min_number = int(input('Мінімальне число = '))
max_number = int(input('Максимальне число = '))
quantity_numbers = int(input('Кількість чисел, які потрібно вибрати = '))

while True:
    # перевірка на то, щоб мінімальне число було більше 1 і менше максимального
    if min_number < 1:
        print('Введіть мінімальне число більше 1')
        min_number = int(input('Нове мінімальне число = '))
        continue
    elif min_number >= max_number:
        print('Введіть мінімальне число менше за максимальне, яке дорівнює', (max_number))
        min_number = int(input('Нове мінімальне число = '))
        continue
    
    # перевірка на то, щоб максимальне число було менше 1000
    if max_number > 1000:
        print('Введіть максимальне число менше або рівно 1000')
        max_number = int(input('Нове максимальне число = '))
        continue

    # перевірка щоб кількість чисел для виводу була не менше різниці максимального і мінімального счисла)
    if quantity_numbers > (max_number - min_number):
        print('Введіть кількість чисел менше або рівно різниці максимального і мінимального, яка дорівнює', max_number - min_number)
        quantity_numbers = int(input('Нова кількість чисел, які потрібно вибрати = '))
        continue

    def get_numbers_ticket():

        # створення списку з числами від мінімального до максималоного
        numbers_list = []
        for i in range(min_number, max_number+1):
            numbers_list.append(i)

        # вибір рандомних чисел зі списку і сортування їх
        get_numbers_ticket = sorted(
            random.sample(numbers_list, quantity_numbers)
            )
        return get_numbers_ticket

    print("Ваші лотерейні числа:", get_numbers_ticket())
    break