import os
import shutil
import threading
import sys

# Функція для копіювання файлів у відповідні піддиректорії за розширенням
def copy_file(file_path, source_dir, target_dir):
    # Отримуємо розширення файлу
    file_extension = os.path.splitext(file_path)[1][1:]  # Отримаємо розширення без крапки
    # Визначаємо цільову директорію для цього розширення
    target_folder = os.path.join(target_dir, file_extension)
    
    # Створюємо директорію, якщо вона ще не існує
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Копіюємо файл у цільову директорію
    shutil.copy(file_path, target_folder)
    print(f"Копіювання файлу: {file_path} до {target_folder}")

# Функція для рекурсивного обходу директорії
def process_directory(source_dir, target_dir):
    threads = []

    for root, _, files in os.walk(source_dir):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            
            # Створюємо новий потік для копіювання файлу
            thread = threading.Thread(target=copy_file, args=(file_path, source_dir, target_dir))
            thread.start()
            threads.append(thread)

    # Очікуємо завершення всіх потоків
    for thread in threads:
        thread.join()
    print("Усі файли успішно скопійовані та відсортовані.")

def main():
    if len(sys.argv) < 2:
        print("Використання: python script.py <source_directory> [<target_directory>]")
        return

    source_dir = sys.argv[1]
    target_dir = sys.argv[2] if len(sys.argv) > 2 else "dist"

    if not os.path.exists(source_dir):
        print(f"Джерельна директорія {source_dir} не існує.")
        return

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    print(f"Обробка файлів із {source_dir} до {target_dir}...")
    process_directory(source_dir, target_dir)
    print("Обробка завершена.")

if __name__ == "__main__":
    main()
