import sys
import types


class _FakeEasyOcrReader:
    def __init__(self, lang_list, **settings):
        self.lang_list = lang_list
        self.settings = settings
        self.result = []
        self.calls = []

    def readtext(self, image, **settings):
        self.calls.append((image, settings))
        return self.result


easyocr = types.ModuleType('easyocr')
easyocr.last_reader = None


def _easyocr_reader_factory(lang_list, **settings):
    easyocr.last_reader = _FakeEasyOcrReader(lang_list, **settings)
    return easyocr.last_reader


easyocr.Reader = _easyocr_reader_factory
sys.modules['easyocr'] = easyocr


class _FakeYoloModel:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.model = types.SimpleNamespace(names={})
        self.results = [types.SimpleNamespace(boxes=[])]
        self.calls = []

    def __call__(self, image):
        self.calls.append(image)
        return self.results


ultralytics = types.ModuleType('ultralytics')
ultralytics.last_model = None


def _yolo_factory(**kwargs):
    ultralytics.last_model = _FakeYoloModel(**kwargs)
    return ultralytics.last_model


ultralytics.YOLO = _yolo_factory
sys.modules['ultralytics'] = ultralytics
