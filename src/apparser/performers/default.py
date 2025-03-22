from apparser.base.app import App
from apparser.instructions.default.base import Instruction
from apparser.performers.base import BasePerformer


class Performer(BasePerformer):
    def __init__(self, app: App):
        super().__init__(app)

    def perform(self, command: Instruction):
        if not isinstance(command, Instruction):
            raise ValueError()

        command(self.app.ui)