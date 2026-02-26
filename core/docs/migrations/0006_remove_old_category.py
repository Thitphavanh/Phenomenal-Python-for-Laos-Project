# Generated manually
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("docs", "0005_migrate_categories_data"),
    ]

    operations = [
        # Remove old category field
        migrations.RemoveField(
            model_name="documentation",
            name="category",
        ),
        # Rename new_category_id column to category_id
        migrations.RenameField(
            model_name="documentation",
            old_name="new_category",
            new_name="category",
        ),
    ]
