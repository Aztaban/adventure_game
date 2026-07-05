from __future__ import annotations

from collections.abc import Sequence


class Dialogue:
    """Track the state of the currently active dialogue."""

    def __init__(self) -> None:
        self._lines: tuple[str, ...] = ()
        self._current_index = 0
        self._is_active = False

    @property
    def is_active(self) -> bool:
        """Return whether a dialogue is currently open."""
        return self._is_active

    @property
    def current_line(self) -> str | None:
        """Return currently displayed line."""
        if not self._is_active:
            return None

        return self._lines[self._current_index]

    def start(self, lines: Sequence[str]) -> None:
        """Start a new dialogue from its first line."""
        if not lines:
            raise ValueError("Dialogue requires at least one line.")

        self._lines = tuple(lines)
        self._current_index = 0
        self._is_active = True

    def advance(self) -> None:
        """Advance to the next line or close at the end."""
        if not self._is_active:
            return

        next_index = self._current_index + 1

        if next_index >= len(self._lines):
            self.close()
            return

        self._current_index = next_index

    def close(self) -> None:
        """Close and reset the active dialogue."""
        self._lines = ()
        self._current_index = 0
        self._is_active = False
