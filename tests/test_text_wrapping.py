from game.ui.text import wrap_text


class FixedWidthFont:
    """Simple text measurer used for wrapping tests."""

    CHARACTER_WIDTH = 10
    LINE_HEIGHT = 20

    def size(self, text: str) -> tuple[int, int]:
        """Return a predictable size for test text."""
        return (len(text) * self.CHARACTER_WIDTH, self.LINE_HEIGHT)


def test_wrap_text_returns_short_text_as_one_line() -> None:
    font = FixedWidthFont()

    lines = wrap_text(font, "short text", maximum_width=100)

    assert lines == ["short text"]


def test_wrap_text_wraps_between_words() -> None:
    font = FixedWidthFont()

    lines = wrap_text(font, "alpha beta gamma", maximum_width=100)

    assert lines == ["alpha beta", "gamma"]


def test_wrap_text_keeps_one_long_word_unbroken() -> None:
    font = FixedWidthFont()

    lines = wrap_text(font, "superlongword", maximum_width=50)

    assert lines == ["superlongword"]


def test_wrap_text_returns_empty_line_for_blank_text() -> None:
    font = FixedWidthFont()

    lines = wrap_text(font, "", maximum_width=100)

    assert lines == [""]
