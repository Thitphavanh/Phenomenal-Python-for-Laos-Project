# Generated manually
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("docs", "0003_create_doccategory"),
    ]

    operations = [
        # Add temporary field to hold new category
        migrations.AddField(
            model_name="documentation",
            name="new_category",
            field=models.ForeignKey(
                blank=True,
                help_text="Documentation category (e.g., Python Basics, Django Advanced)",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="docs.doccategory",
                related_name='documentations',
            ),
        ),
    ]
