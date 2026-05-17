from apparser.instructions.utils.get_all_instructions import get_all_instructions
from apparser.exceptions import InstructionWithIdNotFoundException


def get_instruction_by_id(instruction_id: int):
    """Return an instruction class by its identifier.

    :param instruction_id: Instruction identifier to look up.
    :type instruction_id: int
    :return: Matching instruction class.
    :rtype: type[BaseInstruction]
    :raises TypeError: If ``instruction_id`` has an invalid type.
    :raises ValueError: If ``instruction_id`` is negative.
    :raises InstructionWithIdNotFoundException: If no matching instruction is found.
    """
    if not isinstance(instruction_id, int):
        raise TypeError("id must be an integer")

    if instruction_id < 0:
        raise ValueError("id must be >= 0")

    for instruction in get_all_instructions():
        if instruction.id.fget(None) == instruction_id:
            return instruction

    raise InstructionWithIdNotFoundException(instruction_id)
