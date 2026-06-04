from types import ModuleType

from tests.utils.stubs.ml.chat_stub import ChatStub


class ChatTTSStub(ModuleType):
    def __init__(self) -> None:
        super().__init__("ChatTTS")
        self.reset()

    def reset(self) -> None:
        ChatStub.instances = []
        ChatStub.default_infer_result = []
        ChatStub.default_random_speaker = "random-speaker"
        self.Chat = ChatStub
