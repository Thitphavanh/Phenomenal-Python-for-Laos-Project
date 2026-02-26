# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("docs", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DocCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                (
                    "name_lao",
                    models.CharField(
                        blank=True,
                        help_text="Lao language name",
                        max_length=100,
                        null=True,
                    ),
                ),
                ("slug", models.SlugField(max_length=100, unique=True)),
                (
                    "description",
                    models.TextField(blank=True, help_text="Category description"),
                ),
                (
                    "icon",
                    models.CharField(
                        blank=True, help_text="Icon class or emoji", max_length=50
                    ),
                ),
                ("order", models.IntegerField(default=0, help_text="Display order")),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Documentation Category",
                "verbose_name_plural": "Documentation Categories",
                "ordering": ["order", "name"],
            },
        ),
    ]
