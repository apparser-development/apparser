from apparser.cv.models import CvAllData, CvChangeData, CvBox
from apparser.cv.events import Detected, UnDetected, Moved, Resized


def _is_moved(box: CvBox, old_box: CvBox) -> bool:
    return abs(box.x - old_box.x) > 0 and abs(box.y - old_box.y) > 0


def _is_resized(box: CvBox, old_box: CvBox) -> bool:
    return abs(box.width - old_box.width) > 0 and abs(box.height - old_box.height) > 0


class ChangesChecker:
    def __init__(self):
        self.__old_data: CvAllData | None = None

    def __get_old_box(self, box: CvBox) -> CvBox | None:
        needed_boxes: list[CvBox] = [i for i in self.__old_data.boxes if i.class_id == box.class_id]
        if len(needed_boxes) == 0:
            return None
        return needed_boxes[0]

    def __get_undetected(self, current_data: CvAllData) -> list[CvChangeData]:
        new_ids = [i.class_id for i in current_data.boxes]
        return [CvChangeData(UnDetected, i, i) for i in self.__old_data.boxes if i.class_id not in new_ids]

    def check(self, data: CvAllData) -> list[CvChangeData]:
        result: list[CvChangeData] = self.__get_undetected(data)
        for box in data.boxes:
            old_box = self.__get_old_box(box)
            if old_box is None:
                result.append(CvChangeData(Detected, box, box))
            else:
                if _is_moved(box, old_box):
                    result.append(CvChangeData(Moved, box, old_box))
                if _is_resized(box, old_box):
                    result.append(CvChangeData(Resized, box, old_box))
        return result
