from base.app import App
from instructions.default.base import Instruction
from performers.base import BasePerformer


class Performer(BasePerformer):
    def __init__(self, app: App):
        super().__init__(app)

    def perform(self, command):
        if command is not Instruction:
            raise ValueError

        command.perform(self.app.ui)


