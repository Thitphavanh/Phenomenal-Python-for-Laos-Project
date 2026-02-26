"""
Script to create sample documentation posts with Reflex.dev-style content
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from blog.models import Post, Category
from django.contrib.auth import get_user_model

User = get_user_model()

# Get or create admin user
admin_user = User.objects.filter(is_superuser=True).first()
if not admin_user:
    admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')

# Get categories
python_cat = Category.objects.get(slug='python')
django_cat = Category.objects.get(slug='django')

# Documentation posts data
docs_data = [
    {
        'title': 'Python Basics for Beginners',
        'slug': 'python-basics-for-beginners',
        'category': python_cat,
        'difficulty_level': 'beginner',
        'doc_order': 1,
        'excerpt': 'Learn the fundamental concepts of Python programming language including variables, data types, and control flow.',
        'content': '''## What is Python?

Python is a high-level, interpreted programming language known for its simplicity and readability. It's perfect for beginners and powerful enough for experts.

## Why Learn Python?

Python is one of the most popular programming languages in the world. Here's why:

- **Easy to Learn**: Python's syntax is clear and intuitive
- **Versatile**: Used in web development, data science, AI, and more
- **Great Community**: Millions of developers worldwide
- **High Demand**: Python developers are in high demand

## Installing Python

Before you start coding, you need to install Python on your computer.

### Windows Installation

1. Visit python.org/downloads
2. Download the latest Python installer
3. Run the installer and check "Add Python to PATH"
4. Click "Install Now"

### macOS Installation

macOS comes with Python pre-installed, but it's recommended to install the latest version:

```bash
brew install python3
```

### Linux Installation

Most Linux distributions come with Python. To install the latest version:

```bash
sudo apt-get update
sudo apt-get install python3
```

## Your First Python Program

Let's write a simple "Hello, World!" program:

```python
# This is a comment in Python
print("Hello, World!")
```

Save this in a file called `hello.py` and run it:

```bash
python hello.py
```

## Variables and Data Types

Python has several built-in data types:

### Numbers

```python
# Integer
age = 25

# Float
price = 19.99

# Operations
total = age + price
```

### Strings

```python
# String definition
name = "Python Developer"

# String concatenation
greeting = "Hello, " + name

# String formatting
message = f"My name is {name}"
```

### Booleans

```python
is_active = True
is_complete = False
```

## Control Flow

### If Statements

```python
age = 18

if age >= 18:
    print("You are an adult")
elif age >= 13:
    print("You are a teenager")
else:
    print("You are a child")
```

### Loops

```python
# For loop
for i in range(5):
    print(f"Count: {i}")

# While loop
count = 0
while count < 5:
    print(f"Count: {count}")
    count += 1
```

## Functions

Functions help you organize and reuse code:

```python
def greet(name):
    """Greet a person by name"""
    return f"Hello, {name}!"

# Call the function
message = greet("Alice")
print(message)  # Output: Hello, Alice!
```

## Lists and Dictionaries

### Lists

```python
# Create a list
fruits = ["apple", "banana", "orange"]

# Access items
first_fruit = fruits[0]

# Add items
fruits.append("grape")

# Loop through list
for fruit in fruits:
    print(fruit)
```

### Dictionaries

```python
# Create a dictionary
person = {
    "name": "John",
    "age": 30,
    "city": "Vientiane"
}

# Access values
name = person["name"]

# Add new key-value pair
person["email"] = "john@example.com"
```

## Next Steps

Now that you understand the basics, here's what to learn next:

1. **Object-Oriented Programming**: Learn about classes and objects
2. **File Handling**: Read and write files in Python
3. **Error Handling**: Handle exceptions gracefully
4. **Modules and Packages**: Organize larger projects
5. **Virtual Environments**: Manage project dependencies

## Common Mistakes to Avoid

**Indentation Errors**: Python uses indentation to define code blocks. Make sure your indentation is consistent.

**Variable Naming**: Use descriptive variable names and follow Python naming conventions (lowercase with underscores).

**Not Using Virtual Environments**: Always use virtual environments to manage dependencies for your projects.

## Practice Exercises

1. Write a program that calculates the area of a rectangle
2. Create a function that checks if a number is prime
3. Build a simple calculator using functions
4. Create a to-do list program using lists

## Resources

- Official Python Documentation: docs.python.org
- Python Tutorial: python.org/tutorial
- Practice Problems: leetcode.com, hackerrank.com
''',
    },
    {
        'title': 'Django Getting Started',
        'slug': 'django-getting-started',
        'category': django_cat,
        'difficulty_level': 'beginner',
        'doc_order': 1,
        'excerpt': 'A comprehensive guide to getting started with Django, the Python web framework.',
        'content': '''## What is Django?

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It's used by companies like Instagram, Pinterest, and Mozilla.

## Why Use Django?

Django follows the "batteries included" philosophy, providing everything you need to build a web application:

- **ORM (Object-Relational Mapping)**: Work with databases using Python code
- **Admin Interface**: Automatic admin panel for managing data
- **Authentication**: Built-in user authentication system
- **Security**: Protection against common security threats
- **Scalability**: Handle high traffic with ease

## Prerequisites

Before starting with Django, you should know:

- Basic Python programming
- HTML and CSS basics
- How to use the command line
- Git basics (recommended)

## Installation

### Step 1: Create a Virtual Environment

Always use a virtual environment for Django projects:

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\\Scripts\\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### Step 2: Install Django

With your virtual environment activated:

```bash
pip install django
```

Verify the installation:

```bash
python -m django --version
```

### Step 3: Create Your First Project

```bash
django-admin startproject myproject
cd myproject
```

This creates a project structure:

```
myproject/
    manage.py
    myproject/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```

## Project Structure Explained

### manage.py

A command-line utility for interacting with your Django project:

```bash
# Run development server
python manage.py runserver

# Create database tables
python manage.py migrate

# Create a superuser
python manage.py createsuperuser
```

### settings.py

Contains all project settings:

- Database configuration
- Installed apps
- Middleware
- Templates
- Static files

### urls.py

URL routing for your project:

```python
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
```

## Running the Development Server

Start the development server:

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser. You should see the Django welcome page!

## Creating Your First App

Django projects are organized into apps. Each app serves a specific purpose:

```bash
python manage.py startapp blog
```

This creates an app structure:

```
blog/
    __init__.py
    admin.py
    apps.py
    models.py
    tests.py
    views.py
    migrations/
```

### Register Your App

Add your app to `INSTALLED_APPS` in settings.py:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',  # Add your app here
]
```

## Creating Models

Models define your database structure. In `blog/models.py`:

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
```

### Make Migrations

After creating models, run:

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

## Creating Views

Views handle the logic for your web pages. In `blog/views.py`:

```python
from django.shortcuts import render
from .models import Post

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})
```

## URL Routing

Create `blog/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
]
```

Include in main `urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
]
```

## Templates

Create `blog/templates/blog/post_list.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Blog Posts</title>
</head>
<body>
    <h1>My Blog</h1>
    {% for post in posts %}
        <article>
            <h2>{{ post.title }}</h2>
            <p>{{ post.content }}</p>
            <small>{{ post.created_at }}</small>
        </article>
    {% empty %}
        <p>No posts yet.</p>
    {% endfor %}
</body>
</html>
```

## Django Admin

Django's admin interface is one of its most powerful features.

### Register Your Model

In `blog/admin.py`:

```python
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'content']
```

### Create a Superuser

```bash
python manage.py createsuperuser
```

Visit http://127.0.0.1:8000/admin/ and log in!

## Common Django Commands

Here are the most commonly used Django commands:

```bash
# Run development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Open Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test
```

## Best Practices

**Use Version Control**: Always use Git for your Django projects.

**Environment Variables**: Never commit sensitive data like SECRET_KEY. Use environment variables.

**Virtual Environments**: Always use virtual environments to isolate dependencies.

**Write Tests**: Write tests for your models, views, and forms.

## Next Steps

Now that you have a basic Django project running:

1. Learn about Django forms
2. Understand class-based views
3. Explore Django REST Framework for APIs
4. Learn about Django security best practices
5. Deploy your Django app to production

## Troubleshooting

### Port Already in Use

If port 8000 is already in use:

```bash
python manage.py runserver 8080
```

### Migration Conflicts

If you have migration conflicts:

```bash
python manage.py migrate --fake
```

### Database Issues

To reset your database:

```bash
python manage.py flush
```

## Resources

- Official Django Documentation: docs.djangoproject.com
- Django Tutorial: djangoproject.com/start
- Django Girls Tutorial: tutorial.djangogirls.org
- Two Scoops of Django (Book)
''',
    },
    {
        'title': 'Building Your First Django App',
        'slug': 'building-your-first-django-app',
        'category': django_cat,
        'difficulty_level': 'intermediate',
        'doc_order': 2,
        'excerpt': 'Step-by-step tutorial for building a complete Django web application with user authentication and CRUD functionality.',
        'content': '''## Project Overview

In this tutorial, we'll build a complete task management application with:

- User registration and authentication
- Create, Read, Update, Delete (CRUD) operations
- User-specific data (users only see their own tasks)
- Beautiful UI with TailwindCSS

## Project Setup

### Step 1: Create Project Structure

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install Django
pip install django

# Create project
django-admin startproject taskmanager
cd taskmanager

# Create app
python manage.py startapp tasks
```

### Step 2: Configure Settings

Add the app to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks',  # Our new app
]
```

## Creating Models

### Step 3: Define the Task Model

In `tasks/models.py`:

```python
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
```

### Step 4: Create and Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Setting Up Authentication

### Step 5: Create Authentication Views

Create `tasks/views.py`:

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Task
from .forms import TaskForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')
```

### Step 6: Create Forms

Create `tasks/forms.py`:

```python
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'status', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
```

## CRUD Operations

### Step 7: Create Task Views

Add to `tasks/views.py`:

```python
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Create'})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form, 'action': 'Update'})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'tasks/task_detail.html', {'task': task})
```

### Step 8: Configure URLs

Create `tasks/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('task/new/', views.task_create, name='task_create'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/<int:pk>/edit/', views.task_update, name='task_update'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
```

Update main `urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
]
```

## Creating Templates

### Step 9: Create Base Template

Create `tasks/templates/base.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Task Manager{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{% url 'task_list' %}">Task Manager</a>
            {% if user.is_authenticated %}
                <div class="navbar-nav ms-auto">
                    <span class="navbar-text me-3">Hello, {{ user.username }}</span>
                    <a class="nav-link" href="{% url 'logout' %}">Logout</a>
                </div>
            {% endif %}
        </div>
    </nav>

    <div class="container mt-4">
        {% if messages %}
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        {% endif %}

        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### Step 10: Create Task List Template

Create `tasks/templates/tasks/task_list.html`:

```html
{% extends 'base.html' %}

{% block title %}My Tasks{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1>My Tasks</h1>
    <a href="{% url 'task_create' %}" class="btn btn-primary">New Task</a>
</div>

<div class="row">
    {% for task in tasks %}
    <div class="col-md-4 mb-3">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">{{ task.title }}</h5>
                <p class="card-text">{{ task.description|truncatewords:20 }}</p>
                <div class="mb-2">
                    <span class="badge bg-{{ task.priority == 'high' and 'danger' or task.priority == 'medium' and 'warning' or 'info' }}">
                        {{ task.get_priority_display }}
                    </span>
                    <span class="badge bg-secondary">{{ task.get_status_display }}</span>
                </div>
                <small class="text-muted">Due: {{ task.due_date|default:"No deadline" }}</small>
                <div class="mt-3">
                    <a href="{% url 'task_detail' task.pk %}" class="btn btn-sm btn-info">View</a>
                    <a href="{% url 'task_update' task.pk %}" class="btn btn-sm btn-warning">Edit</a>
                    <a href="{% url 'task_delete' task.pk %}" class="btn btn-sm btn-danger">Delete</a>
                </div>
            </div>
        </div>
    </div>
    {% empty %}
    <div class="col-12">
        <div class="alert alert-info">
            No tasks yet. <a href="{% url 'task_create' %}">Create your first task!</a>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

## Admin Configuration

### Step 11: Configure Admin

In `tasks/admin.py`:

```python
from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'priority', 'status', 'due_date', 'created_at']
    list_filter = ['priority', 'status', 'created_at']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
```

## Testing Your App

### Step 12: Run the Development Server

```bash
python manage.py runserver
```

### Step 13: Create a Superuser

```bash
python manage.py createsuperuser
```

## Security Considerations

**Always Validate User Ownership**: Make sure users can only access their own tasks.

**Use CSRF Protection**: Django's CSRF protection is enabled by default. Never disable it.

**Validate Form Input**: Always use Django forms for user input validation.

**Use HTTPS in Production**: Never send authentication credentials over HTTP.

## Next Steps

Enhance your application with:

1. **Search and Filtering**: Add search functionality for tasks
2. **Task Categories**: Create categories for organizing tasks
3. **Email Notifications**: Send reminders for upcoming deadlines
4. **API Integration**: Build a REST API with Django REST Framework
5. **Frontend Framework**: Use React or Vue.js for the frontend

## Common Issues

### Login Required Not Working

Make sure you've set `LOGIN_URL` in settings.py:

```python
LOGIN_URL = 'login'
```

### Templates Not Found

Check your `TEMPLATES` configuration in settings.py and ensure template directories are correct.

### Static Files Not Loading

Run `collectstatic` in production:

```bash
python manage.py collectstatic
```

## Conclusion

Congratulations! You've built a complete Django application with:

- User authentication
- CRUD operations
- User-specific data
- Admin interface
- Responsive UI

This foundation can be extended to build much more complex applications.
''',
    },
    {
        'title': 'Django Best Practices',
        'slug': 'django-best-practices',
        'category': django_cat,
        'difficulty_level': 'advanced',
        'doc_order': 3,
        'excerpt': 'Learn industry best practices for building secure, scalable, and maintainable Django applications.',
        'content': '''## Introduction

This guide covers essential best practices for Django development, from project structure to deployment. Following these practices will help you build better, more maintainable applications.

## Project Structure

### Organize Your Apps

Keep your Django apps small and focused on a single responsibility:

```
myproject/
├── apps/
│   ├── accounts/       # User management
│   ├── blog/           # Blog functionality
│   ├── api/            # API endpoints
│   └── common/         # Shared utilities
├── config/             # Project settings
│   ├── settings/
│   │   ├── base.py     # Base settings
│   │   ├── local.py    # Local development
│   │   ├── staging.py  # Staging environment
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── static/
├── media/
├── templates/
└── manage.py
```

### Use Environment-Specific Settings

Never hardcode sensitive information. Use environment variables:

```python
# settings/base.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

Use python-decouple or django-environ:

```bash
pip install python-decouple
```

```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

## Model Best Practices

### Use Custom User Models

Always use a custom user model from the start:

```python
# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    def __str__(self):
        return self.email
```

```python
# settings.py
AUTH_USER_MODEL = 'accounts.User'
```

### Add Model Managers

Use custom managers for common queries:

```python
from django.db import models

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

class Post(models.Model):
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20)

    objects = models.Manager()  # Default manager
    published = PublishedManager()  # Custom manager
```

Usage:

```python
# Get all posts
all_posts = Post.objects.all()

# Get only published posts
published_posts = Post.published.all()
```

### Use Model Methods

Add business logic to models:

```python
class Order(models.Model):
    items = models.ManyToManyField('OrderItem')
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def get_subtotal(self):
        return sum(item.get_total() for item in self.items.all())

    def get_total(self):
        subtotal = self.get_subtotal()
        return subtotal - (subtotal * self.discount / 100)

    def apply_discount(self, percentage):
        self.discount = percentage
        self.save()
```

### Index Your Database Fields

Add indexes for frequently queried fields:

```python
class Post(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(unique=True, db_index=True)
    status = models.CharField(max_length=20, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['-created_at']),
        ]
```

## View Best Practices

### Use Class-Based Views

Class-based views promote code reuse:

```python
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.published.all()

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```

### Optimize Database Queries

Use select_related and prefetch_related:

```python
# Bad - N+1 queries
posts = Post.objects.all()
for post in posts:
    print(post.author.name)  # Each iteration queries database

# Good - 1 query with JOIN
posts = Post.objects.select_related('author').all()
for post in posts:
    print(post.author.name)  # No additional queries

# For many-to-many relationships
posts = Post.objects.prefetch_related('tags').all()
```

Use only() and defer() for large models:

```python
# Only fetch specific fields
posts = Post.objects.only('title', 'slug')

# Defer specific fields
posts = Post.objects.defer('content', 'description')
```

### Use Django Debug Toolbar

Install and configure Django Debug Toolbar:

```bash
pip install django-debug-toolbar
```

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ...
]

INTERNAL_IPS = ['127.0.0.1']
```

## Form Best Practices

### Use Model Forms

Let Django generate forms from models:

```python
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'status']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Post.objects.filter(title__iexact=title).exists():
            raise forms.ValidationError('This title already exists')
        return title
```

### Add Form Validation

Implement custom validation:

```python
class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already registered')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')

        return cleaned_data
```

## Security Best Practices

### Always Use CSRF Protection

Never disable CSRF protection in production:

```html
<!-- In forms -->
<form method="POST">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

### Prevent SQL Injection

Always use ORM methods:

```python
# Bad - SQL Injection vulnerability
query = f"SELECT * FROM users WHERE username = '{username}'"

# Good - ORM prevents SQL injection
users = User.objects.filter(username=username)

# If you must use raw SQL, use parameters
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT * FROM users WHERE username = %s", [username])
```

### Use Secure Cookies

Configure secure cookies in production:

```python
# settings/production.py
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Protect Against XSS

Django auto-escapes template variables. For unescaped content, be careful:

```html
<!-- Safe - Auto-escaped -->
<p>{{ user_comment }}</p>

<!-- Dangerous - Use only for trusted content -->
<p>{{ user_comment|safe }}</p>

<!-- Better - Use specific template filters -->
<p>{{ user_comment|linebreaks }}</p>
```

## Testing Best Practices

### Write Comprehensive Tests

Test models, views, and forms:

```python
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author, self.user)

    def test_post_str(self):
        self.assertEqual(str(self.post), 'Test Post')

class PostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_post_list_view(self):
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_post_create_requires_login(self):
        response = self.client.get('/posts/create/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
```

### Use Factory Boy

Create test data easily:

```bash
pip install factory-boy
```

```python
import factory
from .models import Post

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Sequence(lambda n: f'Post {n}')
    content = factory.Faker('paragraph')
    author = factory.SubFactory(UserFactory)

# Usage in tests
post = PostFactory()
user = UserFactory(username='specific_user')
```

## Deployment Best Practices

### Use Gunicorn and Nginx

Production setup:

```bash
pip install gunicorn
```

```bash
# gunicorn_config.py
bind = "127.0.0.1:8000"
workers = 4
timeout = 120
```

Run with:

```bash
gunicorn -c gunicorn_config.py myproject.wsgi:application
```

### Use Celery for Background Tasks

For long-running tasks:

```bash
pip install celery redis
```

```python
# celery.py
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

```python
# tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email_task(subject, message, recipient):
    send_mail(subject, message, 'noreply@example.com', [recipient])
```

### Implement Logging

Configure comprehensive logging:

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/error.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

## Performance Optimization

### Use Caching

Implement Django's caching framework:

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

Cache views:

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def my_view(request):
    # ...
```

Cache template fragments:

```html
{% load cache %}
{% cache 500 sidebar %}
    ... expensive sidebar content ...
{% endcache %}
```

### Use Database Connection Pooling

Configure persistent connections:

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # ...
        'CONN_MAX_AGE': 600,  # 10 minutes
    }
}
```

## Conclusion

Following these best practices will help you:

- Write more maintainable code
- Build more secure applications
- Improve application performance
- Make deployment easier
- Create better tests

Remember: Best practices evolve. Stay updated with Django releases and community recommendations.

## Additional Resources

- Django Documentation: docs.djangoproject.com
- Two Scoops of Django (Book)
- Django Best Practices: django-best-practices.readthedocs.io
- Classy Class-Based Views: ccbv.co.uk
''',
    },
]

# Create documentation posts
print("Creating sample documentation posts...")
for doc_data in docs_data:
    post, created = Post.objects.update_or_create(
        slug=doc_data['slug'],
        defaults={
            'title': doc_data['title'],
            'author': admin_user,
            'category': doc_data['category'],
            'content': doc_data['content'],
            'excerpt': doc_data['excerpt'],
            'post_type': 'doc',
            'difficulty_level': doc_data['difficulty_level'],
            'doc_order': doc_data['doc_order'],
            'status': 'published',
        }
    )
    action = "Created" if created else "Updated"
    print(f"{action}: {post.title}")

print("\nDone! Created/Updated sample documentation posts.")
print("Visit http://127.0.0.1:8000/docs/ to see the documentation.")
