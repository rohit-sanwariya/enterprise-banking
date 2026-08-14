import random


def generate_customer_number():
    return f"CUS{random.randint(1, 999999):06d}"
