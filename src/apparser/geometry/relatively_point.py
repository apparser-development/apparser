class RelativelyPoint:
    def __init__(self, x_percent: float, y_percent: float):
        if not (isinstance(x_percent, float) or isinstance(x_percent, int)):
            raise TypeError('x_percent must be number')

        if  not (isinstance(y_percent, float) or isinstance(y_percent, int)):
            raise TypeError('y_percent must be number')

        if x_percent < -1 or x_percent > 1:
            raise ValueError('x must be between -1 and 1')

        if y_percent < -1 or y_percent > 1:
            raise ValueError('y must be between -1 and 1')

        self.__x_percent = x_percent
        self.__y_percent = y_percent

    @property
    def x(self):
        return self.__x_percent

    @property
    def y(self):
        return self.__y_percent
