from apparser.cv.models import CvAllData, CvChangeData, CvBox
from apparser.cv.events import Detected, UnDetected, Moved, Resized


def _is_moved(box: CvBox, old_box: CvBox) -> bool:
    """Check whether a box position changed.

    :param box: Current box state.
    :type box: CvBox
    :param old_box: Previous box state.
    :type old_box: CvBox
    :return: True if the box coordinates changed.
    :rtype: bool
    """
    return abs(box.x - old_box.x) > 0 or abs(box.y - old_box.y) > 0


def _is_resized(box: CvBox, old_box: CvBox) -> bool:
    """Check whether both box dimensions changed.

    :param box: Current box state.
    :type box: CvBox
    :param old_box: Previous box state.
    :type old_box: CvBox
    :return: True if width and height both changed.
    :rtype: bool
    """
    return abs(box.width - old_box.width) > 0 or abs(box.height - old_box.height) > 0


class ChangesChecker:
    """Compare consecutive reads and produce computer vision change events."""

    def __init__(self):
        """Initialize the checker with an empty previous state."""
        self.__old_data: CvAllData = CvAllData([])

    def __get_old_box(self, box: CvBox) -> CvBox | None:
        """Find the previous box state for the same tracking identifier.

        :param box: Current box state.
        :type box: CvBox
        :return: Matching box from the previous read, if available.
        :rtype: CvBox | None
        """
        if box.track_id is None:
            return None
        needed_boxes: list[CvBox] = [i for i in self.__old_data.boxes if i.track_id == box.track_id]
        if len(needed_boxes) == 0:
            return None
        return needed_boxes[0]

    def __get_undetected(self, current_data: CvAllData) -> list[CvChangeData]:
        """Build events for previously tracked boxes missing from the new read.

        :param current_data: Current computer vision data.
        :type current_data: CvAllData
        :return: Undetected events for disappeared tracked boxes.
        :rtype: list[CvChangeData]
        """
        new_ids = [i.track_id for i in current_data.boxes if i.track_id is not None]
        return [CvChangeData(UnDetected, i, i) for i in self.__old_data.boxes if
                i.track_id not in new_ids and i.track_id is not None]

    def check(self, data: CvAllData) -> list[CvChangeData]:
        """Compare current data with the previous read and return change events.

        :param data: Current computer vision data.
        :type data: CvAllData
        :return: Detected, moved, resized, and undetected events.
        :rtype: list[CvChangeData]
        """
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
        self.__old_data = data
        return result
