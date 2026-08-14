from enum import StrEnum


class TransactionType(StrEnum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(item.value, item.name) for item in cls]
