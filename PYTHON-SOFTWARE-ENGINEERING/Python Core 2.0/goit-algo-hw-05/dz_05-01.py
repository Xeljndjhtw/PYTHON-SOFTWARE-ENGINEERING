# функція для підрахунку числа Фібоначчі
def caching_fibonacci():
    cache = {}
    
    def fibonacci(n):

        # якщо задати значення меньше 0, то повертає нуль
        if n <= 0:
            return 0
        
        # якщо задати значення 1, то повертає 1
        elif n == 1:
            return 1
        
        # в інших випадках починає розрахунок
        elif n in cache:
            return cache[n]
    
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]
    
    return fibonacci

fib = caching_fibonacci()
print(fib(55))
