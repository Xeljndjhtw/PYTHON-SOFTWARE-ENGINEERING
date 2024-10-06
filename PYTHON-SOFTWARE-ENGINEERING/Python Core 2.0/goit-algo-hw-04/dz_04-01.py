
def total_salary(path):
    try:
        with open(path, 'r', encoding='utf-8') as my_file:
            zp = []
            for line in my_file:
                splitted_line = float(line.split(',')[1])
                zp.append(splitted_line)
            total = sum(zp) 
            average = sum(zp) / len(zp) 

    except FileNotFoundError:
        print(f'Файл {path} не знайдено')

    except Exception as e:
        print('Помилка') 

    return total, average    
    
total, average = total_salary('salary_file.txt')
print(f"Загальна сума заробітної плати: {total} \nCередня заробітна плата: {average}")