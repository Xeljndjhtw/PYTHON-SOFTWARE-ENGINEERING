import time
from multiprocessing import Pool, cpu_count

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

def run_parallel(numbers):
    # Використовуємо кількість доступних процесорних ядер
    with Pool(processes=cpu_count()) as pool:
        results = pool.map(factorize, numbers)
    return results

if __name__ == "__main__":
    numbers = [128, 255, 99999, 10651060]

    # Виконання синхронної версії
    start_time = time.time()
    results_sync = run_synchronous(numbers)
    end_time = time.time()
    print("Синхронна версія:")
    print(f"Час виконання: {end_time - start_time:.4f} секунд\n")

    # Виконання багатопроцесорної версії
    start_time = time.time()
    results_parallel = run_parallel(numbers)
    end_time = time.time()
    print("Багатопроцесорна версія:")
    print(f"Час виконання: {end_time - start_time:.4f} секунд")

    # Виведення результатів
    for num, factors in zip(numbers, results_parallel):
        print(f"Фактори числа {num}: {factors}")
