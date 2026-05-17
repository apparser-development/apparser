from apparser.instructions.utils import get_all_instructions


def test_get_all_instructions_collects_only_concrete_instruction_classes() -> None:

    result = get_all_instructions()

    assert len(result) > 0
