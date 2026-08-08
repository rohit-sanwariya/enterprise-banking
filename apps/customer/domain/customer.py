# apps/customer/domain/customer.py
from dataclasses import dataclass
from datetime import UTC, date, datetime
from uuid import UUID

from apps.customer.domain.enums.CustomerStatus import CustomerStatus
from apps.customer.domain.enums.CustomerType import CustomerType
from common.domain.values.email import Email
from common.domain.values.phone_number import PhoneNumber


def ensure_utc(value: datetime | None) -> datetime | None:
    """Ensure a datetime is timezone-aware and normalized to UTC."""
    if value is None:
        return None

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Datetime must be timezone-aware")

    return value.astimezone(UTC)


@dataclass
class Customer:
    """Customer domain entity."""

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    id: UUID
    customer_number: str

    # ------------------------------------------------------------------
    # Customer type
    # ------------------------------------------------------------------

    customer_type: CustomerType

    # ------------------------------------------------------------------
    # Personal info
    # ------------------------------------------------------------------

    first_name: str
    last_name: str
    middle_name: str | None = None
    date_of_birth: date | None = None

    # ------------------------------------------------------------------
    # Contact
    # ------------------------------------------------------------------

    email: Email | None = None
    phone_number: PhoneNumber | None = None

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    status: CustomerStatus = CustomerStatus.ACTIVE

    # ------------------------------------------------------------------
    # Internal audit storage
    #
    # These should not be modified directly by application code.
    # ------------------------------------------------------------------

    _created_at: datetime | None = None
    _updated_at: datetime | None = None
    _closed_at: datetime | None = None

    # ------------------------------------------------------------------
    # Audit properties
    # ------------------------------------------------------------------

    @property
    def created_at(self) -> datetime | None:
        """Return the creation timestamp in UTC."""
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime | None) -> None:
        """Set creation timestamp after validating UTC."""
        self._created_at = ensure_utc(value)

    @property
    def updated_at(self) -> datetime | None:
        """Return the last-update timestamp in UTC."""
        return self._updated_at

    @updated_at.setter
    def updated_at(self, value: datetime | None) -> None:
        """Set update timestamp after validating UTC."""
        self._updated_at = ensure_utc(value)

    @property
    def closed_at(self) -> datetime | None:
        """Return the closure timestamp in UTC."""
        return self._closed_at

    @closed_at.setter
    def closed_at(self, value: datetime | None) -> None:
        """Set closure timestamp after validating UTC."""
        self._closed_at = ensure_utc(value)

    # ------------------------------------------------------------------
    # Derived properties
    # ------------------------------------------------------------------

    @property
    def full_name(self) -> str:
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"

        return f"{self.first_name} {self.last_name}"

    @property
    def is_closed(self) -> bool:
        return self.status == CustomerStatus.CLOSED

    # ------------------------------------------------------------------
    # Internal audit behavior
    # ------------------------------------------------------------------

    def _touch(self) -> None:
        """Update the audit timestamp."""
        self.updated_at = datetime.now(UTC)

    # ------------------------------------------------------------------
    # Domain behavior
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Close the customer."""

        if self.is_closed:
            raise ValueError("Customer already closed")

        now = datetime.now(UTC)

        self.status = CustomerStatus.CLOSED
        self.closed_at = now
        self.updated_at = now
