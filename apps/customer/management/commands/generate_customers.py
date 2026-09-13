import concurrent.futures
import threading
import time

from django.core.management.base import BaseCommand, CommandError
from django.db import close_old_connections
from faker import Faker

from apps.customer.application.services.create_customer import CreateCustomerService
from apps.customer.models import CustomerType

_thread_local = threading.local()


def get_faker() -> Faker:
    """
    Give each worker thread its own Faker instance.

    Faker instances are not shared between worker threads, which avoids
    unnecessary shared state while generating data concurrently.
    """
    if not hasattr(_thread_local, "faker"):
        _thread_local.faker = Faker()

    return _thread_local.faker


def generate_customer(index: int, total: int) -> tuple[bool, str]:
    """
    Generate fake customer data and create the customer through the
    application's existing customer creation service.
    """
    fake = get_faker()

    # Each worker may hold a database connection.
    # Make sure it is healthy before using the ORM.
    close_old_connections()

    try:
        email = f"user_{index}_{fake.email()}"

        customer = CreateCustomerService.execute(
            customer_type=CustomerType.INDIVIDUAL,
            first_name=fake.first_name(),
            middle_name=(
                fake.first_name() if fake.boolean(chance_of_getting_true=30) else None
            ),
            last_name=fake.last_name(),
            date_of_birth=fake.date_of_birth(
                minimum_age=18,
                maximum_age=70,
            ),
            email=email,
            phone_number=fake.msisdn()[:10],
        )

        return (
            True,
            f"[{index + 1}/{total}] Created customer: {customer.email}",
        )

    except Exception as exc:
        return (
            False,
            f"[{index + 1}/{total}] Failed: {exc}",
        )

    finally:
        close_old_connections()


class Command(BaseCommand):
    help = "Generate fake customers using the application's customer service."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=100_000,
            help="Number of customers to generate (default: 100000).",
        )

        parser.add_argument(
            "--workers",
            type=int,
            default=10,
            help="Number of worker threads (default: 10).",
        )

    def handle(self, *args, **options):
        count = options["count"]
        workers = options["workers"]

        if count <= 0:
            raise CommandError("--count must be greater than 0.")

        if workers <= 0:
            raise CommandError("--workers must be greater than 0.")

        self.stdout.write(
            f"Starting creation of {count:,} customers using {workers} workers..."
        )

        start_time = time.monotonic()
        success_count = 0
        failure_count = 0

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=workers,
        ) as executor:
            results = executor.map(
                lambda index: generate_customer(index, count),
                range(count),
            )

            for success, message in results:
                if success:
                    success_count += 1
                    self.stdout.write(self.style.SUCCESS(message))
                else:
                    failure_count += 1
                    self.stdout.write(self.style.ERROR(message))

        elapsed = time.monotonic() - start_time

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Done! Created {success_count:,}/{count:,} customers "
                f"in {elapsed:.2f} seconds."
            )
        )

        if failure_count:
            self.stdout.write(self.style.ERROR(f"Failed: {failure_count:,} customers."))
