class Point:
    def __init__(self, x: int, y: int):
        if x is None:
            raise ValueError('x cannot be None')

        if y is None:
            raise ValueError('y cannot be None')

        if not isinstance(x, int):
            raise ValueError('x must be an integer')

        if not isinstance(y, int):
            raise ValueError('y must be an integer')

        self.__x = x
        self.__y = y

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    def __str__(self):
        return f'(x: {self.x}, y: {self.y})'
