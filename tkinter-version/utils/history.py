"""History management for undo/redo functionality."""
from typing import Any, List
import copy


class HistoryManager:
    """Manages undo/redo history for gradient editing."""

    def __init__(self, max_history: int = 50):
        """Initialize history manager.

        Args:
            max_history: Maximum number of history states to keep
        """
        self.max_history = max_history
        self.history: List[Any] = []
        self.current_index = -1

    def add_state(self, state: Any):
        """Add a new state to history.

        Args:
            state: State object to save (will be deep copied)
        """
        # Remove any states after current index
        if self.current_index < len(self.history) - 1:
            self.history = self.history[:self.current_index + 1]

        # Add new state (deep copy to avoid reference issues)
        self.history.append(copy.deepcopy(state))

        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
        else:
            self.current_index += 1

    def undo(self) -> Any:
        """Undo to previous state.

        Returns:
            Previous state or None if at beginning
        """
        if self.can_undo():
            self.current_index -= 1
            return copy.deepcopy(self.history[self.current_index])
        return None

    def redo(self) -> Any:
        """Redo to next state.

        Returns:
            Next state or None if at end
        """
        if self.can_redo():
            self.current_index += 1
            return copy.deepcopy(self.history[self.current_index])
        return None

    def can_undo(self) -> bool:
        """Check if undo is available."""
        return self.current_index > 0

    def can_redo(self) -> bool:
        """Check if redo is available."""
        return self.current_index < len(self.history) - 1

    def clear(self):
        """Clear all history."""
        self.history.clear()
        self.current_index = -1

    def get_current_state(self) -> Any:
        """Get current state without modifying history."""
        if 0 <= self.current_index < len(self.history):
            return copy.deepcopy(self.history[self.current_index])
        return None
