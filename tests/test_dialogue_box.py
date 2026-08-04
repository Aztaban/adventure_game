from game.input.bindings import InputAction, input_summary_for
from game.ui.dialogue_box import DialogueBox


def test_dialogue_runtime_hint_is_derived_from_binding_catalog() -> None:
    expected = (
        f"{input_summary_for(InputAction.PRIMARY, InputAction.DIALOGUE_ADVANCE)}"
        f" to continue  •  {input_summary_for(InputAction.CANCEL)} to close"
    )

    assert DialogueBox.input_hint() == expected
