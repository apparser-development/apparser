class InstructionNotFoundException(Exception):
    def __init__(self, text: str):
        if text is None:
            super().__init__("Instruction not found.")
        else:
            super().__init__(text)


class InstructionWithIdNotFoundException(InstructionNotFoundException):
    def __init__(self, instruction_id: int):
        super().__init__(f"Instruction with id {instruction_id} was not found.")


class InstructionWithNameNotFoundException(InstructionNotFoundException):
    def __init__(self, instruction_name: str):
        super().__init__(f"Instruction with name {instruction_name} was not found.")
