class InstructionNotFoundException(Exception):
    """Represent a failure to resolve an instruction."""

    def __init__(self, text: str | None):
        """Initialize an instruction lookup exception.

        :param text: Error message text.
        :type text: str | None
        """
        if text is None:
            super().__init__("Instruction not found.")
        else:
            super().__init__(text)


class InstructionWithIdNotFoundException(InstructionNotFoundException):
    """Represent a failure to resolve an instruction by identifier."""

    def __init__(self, instruction_id: int):
        """Initialize an identifier-based instruction lookup exception.

        :param instruction_id: Missing instruction identifier.
        :type instruction_id: int
        """
        super().__init__(f"Instruction with id {instruction_id} was not found.")


class InstructionWithNameNotFoundException(InstructionNotFoundException):
    """Represent a failure to resolve an instruction by name."""

    def __init__(self, instruction_name: str):
        """Initialize a name-based instruction lookup exception.

        :param instruction_name: Missing instruction name.
        :type instruction_name: str
        """
        super().__init__(f"Instruction with name {instruction_name} was not found.")
