from __future__ import annotations

from typing import Protocol


class TextMeasurer(Protocol):
    """Measure rendered text width."""

    def size(self, text: str) -> tuple[int, int]:
        """Return rendered text size."""
        ...


def wrap_text(
    font: TextMeasurer,
    text: str,
    maximum_width: int,
) -> list[str]:
    """Split text into lines that fit inside a maximum width.

    Wrapping happens between words only. A single word wider than the maximum
    width is left unbroken on its own line.
    """
    words = text.split()

    if not words:
        return [""]

    lines: list[str] = []
    current_line = words[0]

    for word in words[1:]:
        candidate = f"{current_line} {word}"

        if font.size(candidate)[0] <= maximum_width:
            current_line = candidate
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)
    return lines
