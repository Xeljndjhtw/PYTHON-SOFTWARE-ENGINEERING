import re

# знаходить всі числа
def generator_numbers(text_to_scan: str):
    
    # загружає регулярку
    pattern = re.compile(r'\d+[.,]?\d+')

    # повертає ітератор і потім віддає кожний елемент
    numbers_iter = pattern.finditer(text_to_scan)
    for number in numbers_iter:
        yield float(number.group())

#  вираховує сумму чисел
def sum_profit(text_to_scan: str, func: callable) -> float:
    return sum(func(text_to_scan))


text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
total_income = sum_profit(text, generator_numbers)
print(f'Загальний дохід: {total_income}')