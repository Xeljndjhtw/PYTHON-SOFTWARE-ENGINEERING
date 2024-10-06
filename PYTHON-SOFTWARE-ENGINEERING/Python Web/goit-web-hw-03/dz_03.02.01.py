import time

def factorize(number):
    factors = []
    for i in range(1, number + 1):
        if number % i == 0:
            factors.append(i)
    return factors

def run_synchronous(numbers):
    results = []
    for number in numbers:
        results.append(factorize(number))
    return results

if __name__ == "__main__":
    numbers = [128, 255, 99999, 10651060]

    start_time = time.time()
    results = run_synchronous(numbers)
    end_time = time.time()

    print("Синхронна версія:")
    for num, factors in zip(numbers, results):
        print(f"Фактори числа {num}: {factors}")
    
    print(f"Час виконання синхронної версії: {end_time - start_time:.4f} секунд")

