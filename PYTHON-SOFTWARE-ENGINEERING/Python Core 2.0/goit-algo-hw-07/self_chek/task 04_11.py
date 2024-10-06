class Point:
    # Клас для представлення точки в двовимірному просторі

    def __init__(self, x, y):
        self.__x = None
        self.__y = None
        self.x = x
        self.y = y

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        if (type(x) == int) or (type(x) == float):
            self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        if (type(y) == int) or (type(y) == float):
            self.__y = y


class Vector:
    # Клас для представлення вектора зі стандартним початком (0, 0)

    def __init__(self, coordinates: Point):
        self.coordinates = coordinates

    def __getitem__(self, index):
        if index == 0:
            return self.coordinates.x
        elif index == 1:
            return self.coordinates.y
        else:
            raise IndexError("Індекс поза межами діапазону: використовуйте 0 для x або 1 для y.")

    def __setitem__(self, index, value):
        if index == 0:
            self.coordinates.x = value
        elif index == 1:
            self.coordinates.y = value
        else:
            raise IndexError("Індекс поза межами діапазону: використовуйте 0 для x або 1 для y.")


# Приклад використання
vector = Vector(Point(1, 10))

# Доступ до координат через об'єкт Point
print(vector.coordinates.x)  # Виведе: 1
print(vector.coordinates.y)  # Виведе: 10

# Зміна координат за допомогою квадратних дужок
vector[0] = 10  # Встановлюємо координату x вектора в 10

# Доступ до координат через квадратні дужки
print(vector[0])  # Виведе: 10
print(vector[1])  # Виведе: 10
