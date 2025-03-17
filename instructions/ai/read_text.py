import numpy

from ai_readers.base import AiReader
from base import Ui
from instructions.ai.base import AiInstruction


class PrintAllText(AiInstruction):
    def __call__(self, ui: Ui, ai: AiReader):
        ui.to_main()
        screenshot = ui.get_screenshot()
        image = numpy.array(screenshot)
        texts = ai.read_image(image)
        for i in texts:
            points_stroke = ""
            for j in i.coordinates:
                points_stroke += str(j) + " "
            print(f'text: "{i.text}", coordinates: {points_stroke}')
