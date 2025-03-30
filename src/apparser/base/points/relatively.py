class RelativelyPoint:
    def __init__(self, x_percent: float, y_percent: float):
        if x_percent is None:
            raise ValueError('x_percent cannot be None')

        if y_percent is None:
            raise ValueError('y_percent cannot be None')

        if x_percent < 0 or x_percent > 1:
            raise ValueError('x must be between 0 and 1')

        if y_percent < 0 or y_percent > 1:
            raise ValueError('y must be between 0 and 1')

        self.__x_percent = x_percent
        self.__y_percent = y_percent

    @property
    def x(self):
        return self.__x_percent

    @property
    def y(self):
        return self.__y_percent