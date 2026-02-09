import abc


class CvEvent(abc.ABC):
    @abc.abstractmethod
    def __str__(self):
        pass