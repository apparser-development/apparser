import sys
import types

from appwindows.geometry import Point
import numpy
import ultralytics


def _install_optional_dependency_stubs():
    if "torch" not in sys.modules:
        torch = types.ModuleType("torch")
        torch.device = lambda value: value

        class _Hub:
            @staticmethod
            def load(**kwargs):
                class _Model:
                    def to(self, device):
                        self.device = device

                    def apply_tts(self, **settings):
                        class _Audio:
                            def detach(self):
                                return self

                            def cpu(self):
                                return self

                            def numpy(self):
                                return numpy.array([], dtype=numpy.float32)

                        return _Audio()

                return _Model(), None

        torch.hub = _Hub()
        sys.modules["torch"] = torch

    if "ChatTTS" not in sys.modules:
        chattts = types.ModuleType("ChatTTS")

        class _Chat:
            class InferCodeParams:
                def __init__(self, spk_emb=None):
                    self.spk_emb = spk_emb

            def load(self, **kwargs):
                pass

            def sample_random_speaker(self):
                return "speaker"

            def infer(self, text, params_infer_code=None, **kwargs):
                return [numpy.array([], dtype=numpy.float32)]

        chattts.Chat = _Chat
        sys.modules["ChatTTS"] = chattts


_install_optional_dependency_stubs()

from apparser.core.ui.coordinates import CoordinatesUi
from apparser.cv.readers.yolo import YoloReader
from tests.utils.cv import CvUi


def test_yolo_reader_init_and_read():
    reader = YoloReader(model="fake.pt")
    fake_box = type(
        "FakeBox",
        (),
        {
            "id": type("FakeId", (), {"item": staticmethod(lambda: 42)})(),
            "cls": type("FakeCls", (), {"item": staticmethod(lambda: 0)})(),
            "xyxy": [type("FakeCoords", (), {"tolist": staticmethod(lambda: [1.2, 2.4, 8.8, 12.9])})()],
        },
    )()
    ultralytics.last_model.model.names = {0: "cat"}
    ultralytics.last_model.results = [type("FakeResult", (), {"boxes": [fake_box]})()]
    image = numpy.array([[1, 2], [3, 4]])
    ui = CvUi(image)

    result = reader.read(ui)

    assert ultralytics.last_model.kwargs == {"model": "fake.pt"}
    assert ultralytics.last_model.calls == []
    assert ultralytics.last_model.track_calls == [(image, True, {})]
    assert len(result.boxes) == 1
    assert result.boxes[0].class_name == "cat"
    assert result.boxes[0].track_id == 42
    assert result.boxes[0].x == 1
    assert result.boxes[0].y == 2
    assert result.boxes[0].width == 7
    assert result.boxes[0].height == 10
    assert isinstance(result.boxes[0].ui, CoordinatesUi)
    assert result.boxes[0].ui.point_to_global(Point(0, 0)) == Point(1, 2)


def test_yolo_reader_reads_zero_tracking_id():
    reader = YoloReader(model="fake.pt")
    fake_box = type(
        "FakeBox",
        (),
        {
            "id": type("FakeId", (), {"item": staticmethod(lambda: 0)})(),
            "cls": type("FakeCls", (), {"item": staticmethod(lambda: 0)})(),
            "xyxy": [type("FakeCoords", (), {"tolist": staticmethod(lambda: [1.2, 2.4, 8.8, 12.9])})()],
        },
    )()
    ultralytics.last_model.model.names = {0: "cat"}
    ultralytics.last_model.results = [type("FakeResult", (), {"boxes": [fake_box]})()]
    result = reader.read(CvUi(numpy.array([[1, 2], [3, 4]])))

    assert result.boxes[0].track_id == 0
