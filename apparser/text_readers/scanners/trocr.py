import importlib
import numpy
from PIL import Image

from apparser.text_readers.scanners.base import BaseTextScanner


class TrocrScanner(BaseTextScanner):
    """Read text from images by using TrOCR."""

    def __init__(self, model_name="microsoft/trocr-base-printed",
                 processor_name=None, device=None):
        """Initialize a TrOCR-backed text scanner.

        :param model_name: Vision encoder-decoder model name.
        :type model_name: str
        :param processor_name: Processor model name. If None, use ``model_name``.
        :type processor_name: str | None
        :param device: Device used for inference. If None, choose CUDA when available.
        :type device: str | None
        """
        transformers = importlib.import_module("transformers")
        torch = importlib.import_module("torch")

        self.__pil_image_module = Image

        if processor_name is None:
            processor_name = model_name

        self.__processor = transformers.TrOCRProcessor.from_pretrained(
            processor_name
        )
        self.__model = transformers.VisionEncoderDecoderModel.from_pretrained(
            model_name
        )

        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.__device = device
        self.__model.to(self.__device)

    def read_image(self, image: numpy.ndarray) -> str:
        """Read text from an image.

        :param image: Image data to process.
        :type image: numpy.ndarray
        :return: Detected text.
        :rtype: str
        """
        pil_image = self.__pil_image_module.fromarray(image).convert("RGB")
        pixel_values = self.__processor(
            images=pil_image, return_tensors="pt"
        ).pixel_values
        pixel_values = pixel_values.to(self.__device)
        generated_ids = self.__model.generate(pixel_values)
        generated_text = self.__processor.batch_decode(
            generated_ids, skip_special_tokens=True
        )[0]
        return generated_text
