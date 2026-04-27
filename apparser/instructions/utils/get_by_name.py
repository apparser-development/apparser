from apparser.instructions.utils._get_all_instructions import _get_all_instructions
from apparser.exceptions import InstructionWithNameNotFoundException


def get_instruction_by_name(instruction_name: str):
    """Return an instruction class by its name.

    :param instruction_name: Instruction class name to look up.
    :type instruction_name: str
    :return: Matching instruction class.
    :rtype: type[BaseInstruction]
    :raises TypeError: If ``instruction_name`` has an invalid type.
    :raises ValueError: If ``instruction_name`` is empty.
    :raises InstructionWithNameNotFoundException: If no matching instruction is found.
    """
    if not isinstance(instruction_name, str):
        raise TypeError("id must be an str")

    if len(instruction_name) <= 0:
        raise ValueError("name is empty")

    for instruction in _get_all_instructions():
        if instruction.__name__ == instruction_name:
            return instruction

    raise InstructionWithNameNotFoundException(instruction_name)
