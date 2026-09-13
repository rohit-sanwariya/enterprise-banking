import concurrent.futures
import time

from django.core.management.base import BaseCommand, CommandError
from django.db import close_old_connections

from apps.accounts.application.services.open_account import OpenAccountService
from apps.customer.models import Customer


def open_account(
    customer_number: str,
    account_type: str,
    currency: str,
) -> tuple[bool, str]:
    """
    Open an account through the application's existing
    OpenAccountService.
    """
    close_old_connections()

    try:
        account = OpenAccountService.execute(
            customer_number=customer_number,
            account_type=account_type,
            currency=currency,
        )

        return (
            True,
            f"Created account {account.account_number} for customer {customer_number}",
        )

    except Exception as exc:
        return (
            False,
            f"Failed for customer {customer_number}: {exc}",
        )

    finally:
        close_old_connections()


class Command(BaseCommand):
    help = "Generate accounts for existing customers."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=1000,
            help="Number of customers to process (default: 100000).",
        )

        parser.add_argument(
            "--workers",
            type=int,
            default=10,
            help="Number of worker threads (default: 10).",
        )

        parser.add_argument(
            "--account-type",
            type=str,
            default="SAVINGS",
            help="Account type to open, e.g. SAVINGS or CURRENT.",
        )

        parser.add_argument(
            "--currency",
            type=str,
            default="INR",
            help="Account currency (default: INR).",
        )

    def handle(self, *args, **options):
        count = options["count"]
        workers = options["workers"]
        account_type = options["account_type"]
        currency = options["currency"]

        if count <= 0:
            raise CommandError("--count must be greater than 0.")

        if workers <= 0:
            raise CommandError("--workers must be greater than 0.")

        self.stdout.write(
            f"Opening {count:,} {account_type} accounts using {workers} workers..."
        )

        # Get only the data the workers need.
        #
        # We intentionally don't pass Customer model instances between
        # threads. OpenAccountService resolves the customer itself.
        customer_numbers = list(
            Customer.objects.exclude(
                accounts__account_type=account_type,
            )
            .order_by("id")
            .values_list("customer_number", flat=True)[:count]
        )

        if not customer_numbers:
            raise CommandError("No customers found.")

        self.stdout.write(f"Found {len(customer_numbers):,} customers to process.")

        start_time = time.monotonic()

        success_count = 0
        failure_count = 0

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=workers,
        ) as executor:
            results = executor.map(
                lambda customer_number: open_account(
                    customer_number,
                    account_type,
                    currency,
                ),
                customer_numbers,
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
                f"Done! Opened {success_count:,}/{len(customer_numbers):,} "
                f"accounts in {elapsed:.2f} seconds."
            )
        )

        if failure_count:
            self.stdout.write(self.style.ERROR(f"Failed: {failure_count:,} accounts."))


#  uv run python manage.py generate_accounts \
#     --count 100000 \
#     --workers 10 \
#     --account-type SAVINGS
