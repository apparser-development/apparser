from types import ModuleType

from tests.utils.stubs.text.fuzz_namespace import FuzzNamespace


class TheFuzzStub(ModuleType):
    def __init__(self) -> None:
        super().__init__("thefuzz")
        self.reset()

    def reset(self) -> None:
        self.fuzz = FuzzNamespace()
