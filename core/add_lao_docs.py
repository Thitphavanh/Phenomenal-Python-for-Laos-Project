#!/usr/bin/env python
"""Add remaining Lao language documentation"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from blog.models import Documentation, Category
from django.contrib.auth.models import User

# Get admin user and category
admin_user = User.objects.get(username='admin')
python_category, _ = Category.objects.get_or_create(slug='python', defaults={'name': 'Python'})

print('=' * 80)
print('📚 CREATING REMAINING LAO DOCUMENTATION')
print('=' * 80)

created_count = 0

# Functions Documentation
if not Documentation.objects.filter(slug='python-functions-lao').exists():
    functions_content = '''# Functions ໃນ Python

## ການແນະນຳ

Function ແມ່ນ block ຂອງ code ທີ່ສາມາດນຳກັບມາໃຊ້ໃໝ່ໄດ້. ມັນຊ່ວຍໃຫ້ code ຂອງເຮົາເປັນລະບຽບ ແລະ ງ່າຍຕໍ່ການບຳລຸງຮັກສາ.

## ການສ້າງ Function

### Function ພື້ນຖານ

```python
# Function ທີ່ບໍ່ມີ parameters
def say_hello():
    print("ສະບາຍດີ!")

# ເອີ້ນໃຊ້ function
say_hello()  # Output: ສະບາຍດີ!
```

### Function ທີ່ມີ Parameters

```python
def greet(name):
    print(f"ສະບາຍດີ, {name}!")

greet("ສົມໃຈ")  # Output: ສະບາຍດີ, ສົມໃຈ!

# ຫຼາຍ parameters
def introduce(name, age):
    print(f"ຂ້ອຍຊື່ {name} ແລະ ອາຍຸ {age} ປີ")

introduce("ສົມໃຈ", 25)
```

### Return Values

```python
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # Output: 8

# Return ຫຼາຍຄ່າ
def get_name():
    first_name = "ສົມ"
    last_name = "ໃຈ"
    return first_name, last_name

fname, lname = get_name()
print(f"{fname} {lname}")
```

## Default Parameters

```python
def greet(name="ເພື່ອນ", greeting="ສະບາຍດີ"):
    print(f"{greeting}, {name}!")

greet()                           # ສະບາຍດີ, ເພື່ອນ!
greet("ສົມໃຈ")                   # ສະບາຍດີ, ສົມໃຈ!
greet("ສົມໃຈ", "ສະບາຍດີຕອນເຊົ້າ")  # ສະບາຍດີຕອນເຊົ້າ, ສົມໃຈ!
```

## Lambda Functions

Lambda ແມ່ນ anonymous function (function ທີ່ບໍ່ມີຊື່):

```python
# Lambda ພື້ນຖານ
square = lambda x: x ** 2
print(square(5))  # 25

# Lambda ກັບຫຼາຍ parameters
add = lambda x, y: x + y
print(add(3, 4))  # 7

# ໃຊ້ກັບ map()
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # [1, 4, 9, 16, 25]
```

## Recursive Functions

Function ທີ່ເອີ້ນຕົວມັນເອງ:

```python
def factorial(n):
    """ຄຳນວນ factorial"""
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))  # 120 (5! = 5×4×3×2×1)

# Fibonacci
def fibonacci(n):
    """ຄຳນວນ Fibonacci ລຳດັບທີ n"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# ສະແດງ 10 ຕົວແຮກຂອງ Fibonacci
for i in range(10):
    print(fibonacci(i), end=" ")
# Output: 0 1 1 2 3 5 8 13 21 34
```

## ສະຫຼຸບ

ໃນບົດຮຽນນີ້ເຮົາໄດ້ຮຽນຮູ້:
- ການສ້າງ functions
- Parameters ແລະ return values
- Default parameters ແລະ keyword arguments
- Lambda functions
- Recursive functions

Functions ແມ່ນພື້ນຖານສຳຄັນຂອງ Python programming. ຝຶກໃຊ້ເລື້ອຍໆເພື່ອໃຫ້ຊຳນານ!
'''

    doc = Documentation.objects.create(
        title='Functions ໃນ Python',
        slug='python-functions-lao',
        author=admin_user,
        category=python_category,
        description='ຮຽນຮູ້ການສ້າງ ແລະ ການໃຊ້ງານ functions ໃນ Python',
        content=functions_content,
        difficulty_level='beginner',
        chapter_number=1,
        section_number=2,
        status='published',
        is_published=True
    )
    print('✅ Created: Functions ໃນ Python')
    created_count += 1
else:
    print('⚠️  Skipping Functions - already exists')

# OOP Documentation
if not Documentation.objects.filter(slug='python-oop-lao').exists():
    oop_content = '''# Object-Oriented Programming ໃນ Python

## ການແນະນຳ

Object-Oriented Programming (OOP) ແມ່ນວິທີການຂຽນໂປຣແກຣມທີ່ໃຊ້ "ວັດຖຸ" (Objects) ເປັນພື້ນຖານ. ມັນຊ່ວຍໃຫ້ code ມີໂຄງສ້າງທີ່ດີ ແລະ ງ່າຍຕໍ່ການບຳລຸງຮັກສາ.

## Classes ແລະ Objects

### ການສ້າງ Class

```python
class Person:
    """Class ທີ່ເປັນຕົວແທນຂອງຄົນ"""

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"ສະບາຍດີ, ຂ້ອຍຊື່ {self.name} ອາຍຸ {self.age} ປີ")

# ສ້າງ object
person1 = Person("ສົມໃຈ", 25)
person2 = Person("ສົມຈິດ", 30)

# ເອີ້ນໃຊ້ method
person1.introduce()  # ສະບາຍດີ, ຂ້ອຍຊື່ ສົມໃຈ ອາຍຸ 25 ປີ
person2.introduce()  # ສະບາຍດີ, ຂ້ອຍຊື່ ສົມຈິດ ອາຍຸ 30 ປີ
```

### Attributes (ຄຸນລັກສະນະ)

```python
class Car:
    def __init__(self, brand, model, year):
        # Instance attributes
        self.brand = brand
        self.model = model
        self.year = year
        self.mileage = 0

    def drive(self, distance):
        self.mileage += distance
        print(f"ຂັບໄປ {distance} km")

    def get_info(self):
        return f"{self.year} {self.brand} {self.model} - {self.mileage} km"

# ສ້າງ object
my_car = Car("Toyota", "Camry", 2023)
print(my_car.get_info())  # 2023 Toyota Camry - 0 km

my_car.drive(100)
print(my_car.get_info())  # 2023 Toyota Camry - 100 km
```

## Inheritance (ການສືບທອດ)

```python
# Parent class (Base class)
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        pass  # Override ໃນ child classes

    def info(self):
        print(f"ນີ້ແມ່ນ {self.name}")

# Child classes
class Dog(Animal):
    def speak(self):
        return "ໂຮ່ງ ໂຮ່ງ!"

class Cat(Animal):
    def speak(self):
        return "ແໝວ ແໝວ!"

class Bird(Animal):
    def speak(self):
        return "ຈິກ ຈິກ!"

# ໃຊ້ງານ
dog = Dog("ໝາ")
cat = Cat("ແມວ")
bird = Bird("ນົກ")

dog.info()           # ນີ້ແມ່ນ ໝາ
print(dog.speak())   # ໂຮ່ງ ໂຮ່ງ!
print(cat.speak())   # ແໝວ ແໝວ!
print(bird.speak())  # ຈິກ ຈິກ!
```

## Encapsulation (ການຫໍ່ຫຸ້ມ)

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance  # Private attribute

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def get_balance(self):
        return self.__balance

    # Property decorator
    @property
    def balance(self):
        return self.__balance

account = BankAccount("ສົມໃຈ", 1000000)
# print(account.__balance)  # Error! Cannot access private
print(account.get_balance())  # OK
print(account.balance)        # OK (via property)
```

## Polymorphism (ຄວາມຫຼາກຫຼາຍ)

```python
class Shape:
    def area(self):
        pass

    def perimeter(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14159 * self.radius

# Polymorphism ໃນການໃຊ້ງານ
shapes = [
    Rectangle(5, 10),
    Circle(7),
    Rectangle(3, 4)
]

for shape in shapes:
    print(f"ພື້ນທີ່: {shape.area():.2f}")
    print(f"ເສັ້ນຮອບວົງ: {shape.perimeter():.2f}")
    print("---")
```

## ສະຫຼຸບ

OOP ໃນ Python ປະກອບດ້ວຍແນວຄິດສຳຄັນ:
- **Classes and Objects**: ການສ້າງແມ່ແບບ ແລະ instances
- **Inheritance**: ການສືບທອດຄຸນສົມບັດ
- **Encapsulation**: ການປົກປິດຂໍ້ມູນ
- **Polymorphism**: ການໃຊ້ງານແບບຫຼາກຫຼາຍ

OOP ຊ່ວຍໃຫ້ code ມີໂຄງສ້າງທີ່ດີ, ງ່າຍຕໍ່ການບຳລຸງຮັກສາ ແລະ ຂະຫຍາຍໄດ້!
'''

    doc = Documentation.objects.create(
        title='Object-Oriented Programming ໃນ Python',
        slug='python-oop-lao',
        author=admin_user,
        category=python_category,
        description='ຮຽນຮູ້ການຂຽນໂປຣແກຣມແບບ Object-Oriented ດ້ວຍ Classes ແລະ Objects',
        content=oop_content,
        difficulty_level='intermediate',
        chapter_number=2,
        section_number=1,
        status='published',
        is_published=True
    )
    print('✅ Created: Object-Oriented Programming ໃນ Python')
    created_count += 1
else:
    print('⚠️  Skipping OOP - already exists')

print('\n' + '=' * 80)
print(f'📊 SUMMARY: Created {created_count} new documentation pages')
print('=' * 80)
print(f'\n🌐 View documentation at: http://127.0.0.1:8000/docs/')
