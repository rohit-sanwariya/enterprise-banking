from enum import Enum


class CustomerStatus(Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    FROZEN = "FROZEN"
    DECEASED = "DECEASED"
    IN_REVIEW = "IN_REVIEW"
