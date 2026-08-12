import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    # FORCES Django to run customer.0001_initial FIRST
    dependencies = [
        ("customer", "0001_initial"),
    ]

    operations = [
        # Create schema before table creation
        migrations.RunSQL(
            sql='CREATE SCHEMA IF NOT EXISTS "accounts";',
            reverse_sql='DROP SCHEMA IF EXISTS "accounts" CASCADE;',
        ),
        migrations.CreateModel(
            name="Account",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("account_number", models.CharField(max_length=20, unique=True)),
                ("account_type", models.CharField(choices=[("SAVINGS", "Savings"), ("CURRENT", "Current")], max_length=20)),
                ("status", models.CharField(choices=[("ACTIVE", "Active"), ("FROZEN", "Frozen"), ("CLOSED", "Closed")], default="ACTIVE", max_length=20)),
                ("currency", models.CharField(default="INR", max_length=3)),
                ("opened_at", models.DateTimeField(auto_now_add=True)),
                ("closed_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=models.deletion.PROTECT,
                        related_name="accounts",
                        to="customer.customer",
                    ),
                ),
            ],
            options={
                "db_table": '"accounts"."account"',
                "ordering": ["-created_at"],
            },
        ),
    ]