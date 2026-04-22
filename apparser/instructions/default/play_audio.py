from apparser.instructions.base import BaseInstruction


class PlayAudio(BaseInstruction):
    @property
    def id(self) -> int:
        return 20

    def perform(self, *args, **kwargs):
        pass