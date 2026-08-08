from dataclasses import dataclass

import phonenumbers
from phonenumbers import PhoneNumberFormat, PhoneNumberType


@dataclass(frozen=True)
class PhoneNumber:
    """Phone number value object with international validation."""

    value: str

    def __post_init__(self):
        if not self._is_valid(self.value):
            raise ValueError(f"Invalid phone number: {self.value}")

    @staticmethod
    def _is_valid(phone: str) -> bool:
        """Validate phone number using Google's phonenumbers library."""
        try:
            parsed = phonenumbers.parse(phone)
            return phonenumbers.is_valid_number(parsed)
        except phonenumbers.NumberParseException:
            return False

    @property
    def parsed(self):
        """Return parsed phone number object."""
        return phonenumbers.parse(self.value)

    @property
    def country_code(self) -> int:
        """Get country code."""
        return self.parsed.country_code

    @property
    def national_number(self) -> str:
        """Get national number (without country code)."""
        return str(self.parsed.national_number)

    @property
    def formatted_e164(self) -> str:
        """Format as E.164 (international format)."""
        return phonenumbers.format_number(self.parsed, PhoneNumberFormat.E164)

    @property
    def formatted_national(self) -> str:
        """Format in national format."""
        return phonenumbers.format_number(self.parsed, PhoneNumberFormat.NATIONAL)

    @property
    def formatted_international(self) -> str:
        """Format in international format."""
        return phonenumbers.format_number(self.parsed, PhoneNumberFormat.INTERNATIONAL)

    @property
    def is_mobile(self) -> bool:
        """Check if it's a mobile number."""
        return phonenumbers.number_type(self.parsed) in [
            PhoneNumberType.MOBILE,
            PhoneNumberType.FIXED_LINE_OR_MOBILE,
        ]

    def __str__(self) -> str:
        return self.formatted_international
