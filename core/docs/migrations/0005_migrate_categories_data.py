# Generated manually
from django.db import migrations


def migrate_categories(apps, schema_editor):
    """Copy blog.Category to docs.DocCategory and update documentation"""
    BlogCategory = apps.get_model('blog', 'Category')
    DocCategory = apps.get_model('docs', 'DocCategory')
    Documentation = apps.get_model('docs', 'Documentation')

    # Get documentation-related categories from blog
    doc_category_slugs = [
        'python-basics', 'python-advanced', 'django-basics',
        'django-advanced', 'web-development', 'data-science',
        'machine-learning', 'python', 'django', 'documentation',
        'python-tutorials'
    ]

    blog_categories = BlogCategory.objects.filter(slug__in=doc_category_slugs)

    # Create mapping from old to new categories
    category_mapping = {}

    # Define Lao names for categories
    lao_names = {
        'python-basics': 'ພື້ນຖານ Python',
        'python-advanced': 'Python ຂັ້ນສູງ',
        'django-basics': 'ພື້ນຖານ Django',
        'django-advanced': 'Django ຂັ້ນສູງ',
        'web-development': 'ການພັດທະນາເວັບ',
        'data-science': 'ວິທະຍາສາດຂໍ້ມູນ',
        'machine-learning': 'ການຮຽນຮູ້ເຄື່ອງຈັກ',
        'python': 'Python',
        'django': 'Django',
        'documentation': 'ເອກະສານ',
        'python-tutorials': 'ບົດສອນ Python',
    }

    for blog_cat in blog_categories:
        # Create corresponding DocCategory
        doc_cat, created = DocCategory.objects.get_or_create(
            slug=blog_cat.slug,
            defaults={
                'name': blog_cat.name,
                'name_lao': lao_names.get(blog_cat.slug, ''),
                'description': blog_cat.description or '',
                'order': 0,
                'is_active': True,
            }
        )
        category_mapping[blog_cat.id] = doc_cat

    # Update all Documentation entries
    for doc in Documentation.objects.all():
        if doc.category_id and doc.category_id in category_mapping:
            doc.new_category = category_mapping[doc.category_id]
            doc.save()


def reverse_migrate(apps, schema_editor):
    """Reverse migration - clear new_category field"""
    Documentation = apps.get_model('docs', 'Documentation')
    Documentation.objects.all().update(new_category=None)


class Migration(migrations.Migration):

    dependencies = [
        ("docs", "0004_add_temp_category_field"),
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(migrate_categories, reverse_migrate),
    ]
