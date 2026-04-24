import sys
import types

import easyocr
import numpy
from appwindows.geometry import Point


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

from apparser.text_readers.easy_ocr import EasyOcrReader
from apparser.text_readers.models.text_data import TextData
import apparser.text_readers.paddle_ocr as paddle_ocr_module
from apparser.text_readers.paddle_ocr import PaddleTextReader
from apparser.text_readers.screens_controller import ScreensController
from apparser.text_readers.white_black_reader import WhiteBlackReader
from tests.utils.readers import FakeTextReader


def test_easy_ocr_reader_default_lang_and_read_image():
    reader = EasyOcrReader(gpu=False)
    image = numpy.array([[1, 2], [3, 4]])
    easyocr.last_reader.result = [
        (
            [(1.2, 2.8), (3.9, 4.1), (5.7, 6.3), (7.4, 8.6)],
            "hello",
            0.99,
        )
    ]

    result = reader.read_image(image, detail=1)

    assert easyocr.last_reader.lang_list == ["en"]
    assert easyocr.last_reader.settings == {"gpu": False}
    assert easyocr.last_reader.calls == [(image, {"detail": 1})]
    assert result == [
        TextData(
            "hello",
            [Point(1, 2), Point(3, 4), Point(5, 6), Point(7, 8)],
        )
    ]


def test_screens_controller_caches_images():
    ai_reader = FakeTextReader()
    ai_reader.result = [TextData("cached", [Point(0, 0)])]
    controller = ScreensController(ai_reader)
    image = numpy.array([[1, 2], [3, 4]])

    first = controller.read_image(image)
    second = controller.read_image(image.copy())

    assert first == ai_reader.result
    assert second == ai_reader.result
    assert len(ai_reader.calls) == 1


def test_white_black_reader_converts_image_to_grayscale():
    ai_reader = FakeTextReader()
    ai_reader.result = [TextData("gray", [Point(0, 0)])]
    image = numpy.array([[[255, 0, 0], [0, 255, 0]]], dtype=numpy.uint8)

    result = WhiteBlackReader(ai_reader).read_image(image)

    assert result == ai_reader.result
    assert len(ai_reader.calls) == 1
    assert ai_reader.calls[0].ndim == 2


def test_paddle_text_reader_predict_read_image(monkeypatch):
    created = {}

    class FakePaddleOCR:
        def __init__(self, lang, **settings):
            self.lang = lang
            self.settings = settings
            self.calls = []
            created["reader"] = self

        def predict(self, image, **settings):
            self.calls.append((image, settings))
            return [
                {
                    "rec_texts": ["hello"],
                    "rec_polys": [
                        [(1.2, 2.8), (3.9, 4.1), (5.7, 6.3), (7.4, 8.6)],
                    ],
                },
                types.SimpleNamespace(
                    res={
                        "rec_texts": ["world"],
                        "dt_polys": [
                            [(10.2, 11.8), (12.9, 13.1), (14.7, 15.3), (16.4, 17.6)],
                        ],
                    }
                ),
            ]

    monkeypatch.setattr(
        paddle_ocr_module.importlib,
        "import_module",
        lambda name: types.SimpleNamespace(PaddleOCR=FakePaddleOCR),
    )

    image = numpy.array([[1, 2], [3, 4]])
    reader = PaddleTextReader(lang="ru", use_doc_orientation_classify=False)
    result = reader.read_image(image, cls=True)

    assert created["reader"].lang == "ru"
    assert created["reader"].settings == {"use_doc_orientation_classify": False}
    assert created["reader"].calls == [(image, {"cls": True})]
    assert result == [
        TextData(
            "hello",
            [Point(1, 2), Point(3, 4), Point(5, 6), Point(7, 8)],
        ),
        TextData(
            "world",
            [Point(10, 11), Point(12, 13), Point(14, 15), Point(16, 17)],
        ),
    ]


def test_paddle_text_reader_ocr_read_image(monkeypatch):
    created = {}

    class FakePaddleOCR:
        def __init__(self, lang, **settings):
            self.lang = lang
            self.settings = settings
            self.calls = []
            created["reader"] = self

        def ocr(self, image, **settings):
            self.calls.append((image, settings))
            return [[
                (
                    [(1.2, 2.8), (3.9, 4.1), (5.7, 6.3), (7.4, 8.6)],
                    ("hello", 0.99),
                ),
                None,
            ]]

    monkeypatch.setattr(
        paddle_ocr_module.importlib,
        "import_module",
        lambda name: types.SimpleNamespace(PaddleOCR=FakePaddleOCR),
    )

    image = numpy.array([[1, 2], [3, 4]])
    reader = PaddleTextReader(lang="en", use_angle_cls=True)
    result = reader.read_image(image, det=True)

    assert created["reader"].lang == "en"
    assert created["reader"].settings == {"use_angle_cls": True}
    assert created["reader"].calls == [(image, {"det": True})]
    assert result == [
        TextData(
            "hello",
            [Point(1, 2), Point(3, 4), Point(5, 6), Point(7, 8)],
        )
    ]
