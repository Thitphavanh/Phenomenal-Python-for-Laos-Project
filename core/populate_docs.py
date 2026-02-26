import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from blog.models import Post, Category
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()
# Get or create a superuser for authoring
user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})
if created:
    user.set_password('admin')
    user.save()

# Create Categories
doc_cat, _ = Category.objects.get_or_create(name='Documentation', slug='documentation')
python_cat, _ = Category.objects.get_or_create(name='Python', slug='python')
django_cat, _ = Category.objects.get_or_create(name='Django', slug='django')

# Docs Content
docs = [
    {
        'title': 'Install Python',
        'content': """
## Installing Python

Python is a versatile programming language. Here is how to install it:

### Windows
1. Download the installer from python.org.
2. Run the installer and check "Add Python to PATH".
3. Click "Install Now".

### macOS
1. Install via Homebrew: `brew install python`
2. Verify with `python3 --version`.

### Linux
1. Ubuntu/Debian: `sudo apt install python3`
""",
        'category': python_cat,
        'post_type': 'doc',
        'slug': 'install-python'
    },
    {
        'title': 'Install Django',
        'content': """
## Installing Django

Django is a high-level Python web framework.

### Prerequisites
- Python installed (see 'Install Python').
- pip (Python package manager).

### Installation
Run the following command in your terminal:

```bash
pip install django
```

To verify the installation:

```bash
python -m django --version
```
""",
        'category': django_cat,
        'post_type': 'doc',
        'slug': 'install-django'
    }
]

for doc_data in docs:
    post, created = Post.objects.get_or_create(
        slug=doc_data['slug'],
        defaults={
            'title': doc_data['title'],
            'content': doc_data['content'],
            'author': user,
            'status': 'published',
            'category': doc_data['category'],
            'post_type': doc_data['post_type'], 
            'excerpt': doc_data['content'][:100] + '...'
        }
    )
    if created:
        print(f"Created doc: {post.title}")
    else:
        # Update type just in case
        post.post_type = 'doc'
        post.save()
        print(f"Updated doc: {post.title}")

print("Documentation population complete.")
