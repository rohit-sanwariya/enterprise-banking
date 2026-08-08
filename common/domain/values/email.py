import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    """Email value object — shared across domains."""

    value: str

    def __post_init__(self):
        if not self._is_valid(self.value):
            raise ValueError(f"Invalid email: {self.value}")

    @staticmethod
    def _is_valid(email: str) -> bool:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @property
    def domain(self) -> str:
        """Extract domain from email."""
        return self.value.split("@")[1]

    def __str__(self) -> str:
        return self.value
