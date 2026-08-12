import secrets


def generate_account_number() -> str:
    return f"ACC{secrets.randbelow(10**10):010d}"
