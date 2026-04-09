from apparser.instructions.utils._get_all_instructions import _get_all_instructions


def get_instruction_by_name(name: str):
    if not isinstance(name, str):
        raise TypeError("id must be an str")

    if len(name) <= 0:
        raise ValueError("name is empty")

    for instruction in _get_all_instructions():
        if instruction.__name__ == name:
            return instruction

    return None
