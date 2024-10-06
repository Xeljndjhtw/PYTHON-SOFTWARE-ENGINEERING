class Point:
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

    def __str__(self):
        return f"Point({self.x},{self.y})"


class Vector:
    def __init__(self, coordinates: Point):
        self.coordinates = coordinates

    def __setitem__(self, index, value):
        if index == 0:
            self.coordinates.x = value
        if index == 1:
            self.coordinates.y = value

    def __getitem__(self, index):
        if index == 0:
            return self.coordinates.x
        if index == 1:
            return self.coordinates.y

    def __call__(self, value=None):
        if value:
            self.coordinates.x = self.coordinates.x * value
            self.coordinates.y = self.coordinates.y * value
        return self.coordinates.x, self.coordinates.y

    def __add__(self, other):
        # Додавання векторів: (x1 + x2, y1 + y2)
        new_x = self.coordinates.x + other.coordinates.x
        new_y = self.coordinates.y + other.coordinates.y
        return Vector(Point(new_x, new_y))

    def __sub__(self, other):
        # Віднімання векторів: (x1 - x2, y1 - y2)
        new_x = self.coordinates.x - other.coordinates.x
        new_y = self.coordinates.y - other.coordinates.y
        return Vector(Point(new_x, new_y))
    def __mul__(self, other):
        # Скалярний добуток векторів: x1*x2 + y1*y2
        return self.coordinates.x * other.coordinates.x + self.coordinates.y * other.coordinates.y

        
        
        

    def __str__(self):
        return f"Vector({self.coordinates.x},{self.coordinates.y})"