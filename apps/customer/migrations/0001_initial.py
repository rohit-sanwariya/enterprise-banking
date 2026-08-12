import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        # Ensure PostgreSQL customer schema exists
        migrations.RunSQL(
            sql='CREATE SCHEMA IF NOT EXISTS "customer";',
            reverse_sql='DROP SCHEMA IF EXISTS "customer" CASCADE;',
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("customer_number", models.CharField(editable=False, max_length=20, unique=True)),
                ("customer_type", models.CharField(choices=[("INDIVIDUAL", "Individual"), ("BUSINESS", "Business")], default="INDIVIDUAL", max_length=20)),
                ("first_name", models.CharField(max_length=100)),
                ("middle_name", models.CharField(blank=True, max_length=100, null=True)),
                ("last_name", models.CharField(max_length=100)),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                ("email", models.EmailField(blank=True, max_length=255, null=True)),
                ("phone_number", models.CharField(blank=True, max_length=20, null=True)),
                ("status", models.CharField(choices=[("ACTIVE", "Active"), ("CLOSED", "Closed"), ("DORMANT", "Dormant"), ("FROZEN", "Frozen"), ("DECEASED", "Deceased")], default="ACTIVE", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("closed_at", models.DateTimeField(blank=True, null=True)),
            ],
            options={
                "db_table": '"customer"."customer"',
                "ordering": ["-created_at"],
            },
        ),
    ]