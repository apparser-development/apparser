import abc

from base.app import App
from instructions.default.base import Instruction


class BasePerformer(abc.ABC):
    def __init__(self, app: App):
        self.__app = app

    @abc.abstractmethod
    def perform(self, command: Instruction):
        pass

    def perform_all(self, commands: list):
        for i in commands:
            self.perform(i)

    @property
    def app(self):
        return self.__app