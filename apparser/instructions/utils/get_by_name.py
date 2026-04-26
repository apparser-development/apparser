from apparser.instructions.utils._get_all_instructions import _get_all_instructions
from apparser.exceptions import InstructionWithNameNotFoundException


def get_instruction_by_name(instruction_name: str):
    if not isinstance(instruction_name, str):
        raise TypeError("id must be an str")

    if len(instruction_name) <= 0:
        raise ValueError("name is empty")

    for instruction in _get_all_instructions():
        if instruction.__name__ == instruction_name:
            return instruction

    raise InstructionWithNameNotFoundException(instruction_name)
