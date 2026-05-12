import numpy

from apparser.text_readers.paddle import (
    PaddleTextReader,
)
from tests.utils import paddleocr_stub


def test_paddle_text_reader_uses_predict_when_available() -> None:
    reader = PaddleTextReader(lang="ru")
    instance = paddleocr_stub.PaddleOCR.instances[0]
    instance.predict_result = [
        {
            "rec_texts": ["hello"],
            "rec_polys": [[[1, 1], [2, 2], [3, 3], [4, 4]]],
        }
    ]

    result = reader.read_image(numpy.zeros((2, 2, 3), dtype=numpy.uint8), use_doc_orientation_classify=False)

    assert instance.lang == "ru"
    assert instance.predict_calls[0]["settings"] == {"use_doc_orientation_classify": False}
    assert result[0].text == "hello"
