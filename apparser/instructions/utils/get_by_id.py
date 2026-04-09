from apparser.instructions.utils._get_all_instructions import _get_all_instructions


def get_instruction_by_id(id: int):
    if not isinstance(id, int):
        raise TypeError("id must be an integer")

    if id < 0:
        raise ValueError("id must be >= 0")

    for instruction in _get_all_instructions():
        if instruction.id.fget(None) == id:
            return instruction

    return None
