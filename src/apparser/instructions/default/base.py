import abc

from apparser.base import Ui


class Instruction(abc.ABC):
    @abc.abstractmethod
    def perform(self, ui: Ui, *args, **kwargs):
        """
        Perform current instruction

        app = App("some.exe")

        instruction = Instruction()

        instruction.perform(app.ui)
        """
        pass
