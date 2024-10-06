def get_cats_info(path):

    try:
        file = open(path, 'r', encoding='utf-8')
            
        cats = []
        while True:
            line = file.readline(0)
            for cat_info in file:

                # заготовуємо ссилки 
                cat_id = cat_info.split(',')[0]
                cat_name = cat_info.split(',')[1]
                cat_age = cat_info.strip().split(',')[2]

                # іменуємо ссилки
                cat = {}
                cat_info = {'id': cat_id, 'name': cat_name, 'age': cat_age}
                cat.update(cat_info)
            
                cats.append(cat)
            if not line:
                break

    except FileNotFoundError:
        print(f'Файл {path} не знайдено')

    except Exception as e:
        print('Помилка')  

    finally:
        file.close()   

    return cats

cats_info = get_cats_info('cats_info.txt')
print(cats_info)
        
        

