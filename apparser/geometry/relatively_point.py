class RelativelyPoint:
    """Store coordinates as relative values in the range from -1 to 1."""

    def __init__(self, x_percent: float, y_percent: float):
        """Initialize a relative point.

        :param x_percent: Relative X coordinate.
        :type x_percent: float
        :param y_percent: Relative Y coordinate.
        :type y_percent: float
        :raises TypeError: If either coordinate has an invalid type.
        :raises ValueError: If either coordinate is outside the inclusive range from -1 to 1.
        """
        if not (isinstance(x_percent, float) or isinstance(x_percent, int)):
            raise TypeError('x_percent must be number')

        if  not (isinstance(y_percent, float) or isinstance(y_percent, int)):
            raise TypeError('y_percent must be number')

        if x_percent < -1 or x_percent > 1:
            raise ValueError('x_percent must be between -1 and 1')

        if y_percent < -1 or y_percent > 1:
            raise ValueError('y_percent must be between -1 and 1')

        self.__x_percent = x_percent
        self.__y_percent = y_percent

    @property
    def x(self):
        """Return the relative X coordinate.

        :return: Relative X coordinate.
        :rtype: float
        """
        return self.__x_percent

    @property
    def y(self):
        """Return the relative Y coordinate.

        :return: Relative Y coordinate.
        :rtype: float
        """
        return self.__y_percent
