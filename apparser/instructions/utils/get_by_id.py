from apparser.instructions.utils._get_all_instructions import _get_all_instructions
from apparser.exceptions import InstructionWithIdNotFoundException


def get_instruction_by_id(instruction_id: int):
    if not isinstance(instruction_id, int):
        raise TypeError("id must be an integer")

    if instruction_id < 0:
        raise ValueError("id must be >= 0")

    for instruction in _get_all_instructions():
        if instruction.id.fget(None) == instruction_id:
            return instruction

    raise InstructionWithIdNotFoundException(instruction_id)
