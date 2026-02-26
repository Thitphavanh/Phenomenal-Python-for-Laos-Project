#!/usr/bin/env python
"""
Create additional Lao language documentation
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from blog.models import Documentation, Category
from django.contrib.auth.models import User

# Documentation content in Lao
DOCS = [
    {
        'title': 'Python Basics: ພາກສະລັບພື້ນຖານ',
        'slug': 'python-basics-lao',
        'category_name': 'Python',
        'difficulty': 'beginner',
        'chapter': 1,
        'section': 1,
        'description': 'ຮຽນຮູ້ພື້ນຖານຂອງ Python ຕັ້ງແຕ່ຕົວແປ, ປະເພດຂໍ້ມູນ, ຈົນເຖິງ operators',
        'content': """# Python Basics: ພາກສະລັບພື້ນຖານ

## ການແນະນຳ

Python ແມ່ນພາສາທີ່ງ່າຍຕໍ່ການຮຽນຮູ້ແລະມີ syntax ທີ່ອ່ານງ່າຍ. ໃນບົດຮຽນນີ້ ພວກເຮົາຈະຮຽນຮູ້ພື້ນຖານຂອງ Python.

## ຕົວແປ (Variables)

ຕົວແປແມ່ນບ່ອນເກັບຂໍ້ມູນໃນ memory. ໃນ Python ບໍ່ຈຳເປັນຕ້ອງປະກາດປະເພດຂໍ້ມູນ:

```python
# ສ້າງຕົວແປ
name = "ສົມໃຈ"
age = 25
height = 1.75
is_student = True

# ສະແດງຜົນ
print(f"ຊື່: {name}")
print(f"ອາຍຸ: {age} ປີ")
print(f"ສູງ: {height} ແມັດ")
```

## ປະເພດຂໍ້ມູນ (Data Types)

Python ມີປະເພດຂໍ້ມູນພື້ນຖານດັ່ງນີ້:

### 1. Numbers (ຕົວເລກ)

```python
# Integer (ເລກຈຳນວນເຕັມ)
count = 10
negative = -5

# Float (ເລກທົດສະນິຍົມ)
price = 99.99
temperature = -10.5

# Complex (ເລກສະກຸນ)
complex_num = 3 + 4j
```

### 2. Strings (ຂໍ້ຄວາມ)

```python
# String ພື້ນຖານ
message = "ສະບາຍດີ"
greeting = 'ຍິນດີຕ້ອນຮັບ'

# Multi-line string
description = '''
    ນີ້ແມ່ນຂໍ້ຄວາມ
    ທີ່ມີຫຼາຍບັນທັດ
'''

# String concatenation
full_name = "ສົມ" + " " + "ໃຈ"

# String formatting
age = 25
text = f"ຂ້ອຍອາຍຸ {age} ປີ"
```

### 3. Boolean (ຄ່າຄວາມຈິງ)

```python
is_adult = True
is_student = False

# Boolean operations
has_license = True
can_drive = has_license and is_adult
```

### 4. Lists (ລາຍການ)

```python
# ສ້າງ list
fruits = ["ໝາກມ່ວງ", "ໝາກກ້ວຍ", "ໝາກກ່ຽງ"]
numbers = [1, 2, 3, 4, 5]
mixed = ["text", 123, True, 3.14]

# ເຂົ້າເຖິງຂໍ້ມູນ
first_fruit = fruits[0]  # "ໝາກມ່ວງ"
last_fruit = fruits[-1]   # "ໝາກກ່ຽງ"

# ເພີ່ມຂໍ້ມູນ
fruits.append("ໝາກກ້ວຍໂອ່ງ")

# ລຶບຂໍ້ມູນ
fruits.remove("ໝາກກ້ວຍ")
```

## Operators (ຕົວດຳເນີນການ)

### Arithmetic Operators

```python
# ການຄິດໄລ່ພື້ນຖານ
a = 10
b = 3

addition = a + b        # 13
subtraction = a - b     # 7
multiplication = a * b  # 30
division = a / b        # 3.333...
floor_division = a // b # 3
modulus = a % b        # 1
power = a ** b         # 1000
```

### Comparison Operators

```python
x = 10
y = 5

print(x == y)  # False (ເທົ່າກັນ)
print(x != y)  # True (ບໍ່ເທົ່າກັນ)
print(x > y)   # True (ຫຼາຍກວ່າ)
print(x < y)   # False (ນ້ອຍກວ່າ)
print(x >= y)  # True (ຫຼາຍກວ່າຫຼືເທົ່າກັນ)
print(x <= y)  # False (ນ້ອຍກວ່າຫຼືເທົ່າກັນ)
```

### Logical Operators

```python
# AND
is_adult = True
has_id = True
can_enter = is_adult and has_id  # True

# OR
has_cash = False
has_card = True
can_pay = has_cash or has_card   # True

# NOT
is_closed = False
is_open = not is_closed          # True
```

## Input/Output

### ຮັບຂໍ້ມູນຈາກຜູ້ໃຊ້

```python
# Input ພື້ນຖານ
name = input("ກະລຸນາປ້ອນຊື່: ")
print(f"ສະບາຍດີ, {name}!")

# Input ເປັນຕົວເລກ
age = int(input("ປ້ອນອາຍຸຂອງທ່ານ: "))
next_year_age = age + 1
print(f"ປີໜ້າທ່ານຈະອາຍຸ {next_year_age} ປີ")
```

### ສະແດງຜົນ

```python
# Print ພື້ນຖານ
print("ສະບາຍດີ")

# Print ຫຼາຍຄ່າ
name = "ສົມໃຈ"
age = 25
print("ຊື່:", name, "ອາຍຸ:", age)

# F-strings (ແນະນຳ)
print(f"ຊື່: {name}, ອາຍຸ: {age}")

# Format method
print("ຊື່: {}, ອາຍຸ: {}".format(name, age))
```

## Control Flow (ການຄວບຄຸມການໄຫຼຂອງໂປຣແກຣມ)

### If-Else Statements

```python
age = int(input("ອາຍຸຂອງທ່ານ: "))

if age >= 18:
    print("ທ່ານເປັນຜູ້ໃຫຍ່ແລ້ວ")
elif age >= 13:
    print("ທ່ານເປັນໄວລຸ້ນ")
else:
    print("ທ່ານຍັງເປັນເດັກ")
```

### For Loops

```python
# Loop ຜ່ານ list
fruits = ["ໝາກມ່ວງ", "ໝາກກ້ວຍ", "ໝາກກ່ຽງ"]
for fruit in fruits:
    print(f"ຂ້ອຍຊອບກິນ {fruit}")

# Loop ຜ່ານຕົວເລກ
for i in range(5):
    print(f"ເລກ {i}")

# Loop ພ້ອມ index
for index, fruit in enumerate(fruits):
    print(f"{index + 1}. {fruit}")
```

### While Loops

```python
count = 0
while count < 5:
    print(f"ນັບ: {count}")
    count += 1

# While loop ກັບ break
while True:
    answer = input("ທ່ານຕ້ອງການອອກບໍ່? (ແມ່ນ/ບໍ່): ")
    if answer == "ແມ່ນ":
        break
    print("ດີ, ສືບຕໍ່...")
```

## ແບບຝຶກຫັດ

ລອງຂຽນໂປຣແກຣມນີ້:

```python
# ໂປຣແກຣມຄິດໄລ່ BMI
print("=== ຄຳນວນດັດຊະນີມວນກາຍ (BMI) ===")

weight = float(input("ນ້ຳໜັກ (kg): "))
height = float(input("ສ່ວນສູງ (m): "))

bmi = weight / (height ** 2)

print(f"\\nBMI ຂອງທ່ານ: {bmi:.2f}")

if bmi < 18.5:
    print("ທ່ານຜອມເກີນໄປ")
elif bmi < 25:
    print("ນ້ຳໜັກປົກກະຕິ")
elif bmi < 30:
    print("ນ້ຳໜັກເກີນ")
else:
    print("ໂຮກອ້ວນ")
```

## ສະຫຼຸບ

ໃນບົດຮຽນນີ້ເຮົາໄດ້ຮຽນຮູ້:
- ຕົວແປ ແລະ ປະເພດຂໍ້ມູນ
- Operators ຕ່າງໆ
- Input/Output
- Control Flow (if/else, loops)

ຕໍ່ໄປເຮົາຈະຮຽນຮູ້ກ່ຽວກັບ Data Structures ແລະ Functions!
"""
    },
    {
        'title': 'Functions ໃນ Python',
        'slug': 'python-functions-lao',
        'category_name': 'Python',
        'difficulty': 'beginner',
        'chapter': 1,
        'section': 2,
        'description': 'ຮຽນຮູ້ການສ້າງ ແລະ ການໃຊ້ງານ functions ໃນ Python',
        'content': """# Functions ໃນ Python

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

## Keyword Arguments

```python
def print_info(name, age, city):
    print(f"ຊື່: {name}")
    print(f"ອາຍຸ: {age}")
    print(f"ເມືອງ: {city}")

# ເອີ້ນໃຊ້ດ້ວຍ keyword arguments
print_info(name="ສົມໃຈ", age=25, city="ວຽງຈັນ")

# ສາມາດສັບຕຳແໜ່ງໄດ້
print_info(city="ວຽງຈັນ", name="ສົມໃຈ", age=25)
```

## *args ແລະ **kwargs

### *args (Variable Positional Arguments)

```python
def sum_all(*numbers):
    total = 0
    for num in numbers:
        total += num
    return total

print(sum_all(1, 2, 3))          # 6
print(sum_all(1, 2, 3, 4, 5))    # 15
```

### **kwargs (Variable Keyword Arguments)

```python
def print_info(**info):
    for key, value in info.items():
        print(f"{key}: {value}")

print_info(name="ສົມໃຈ", age=25, city="ວຽງຈັນ")
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

# ໃຊ້ກັບ filter()
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)  # [2, 4]
```

## Docstrings

```python
def calculate_bmi(weight, height):
    """
    ຄຳນວນດັດຊະນີມວນກາຍ (BMI)

    Args:
        weight (float): ນ້ຳໜັກເປັນກິໂລກຣາມ
        height (float): ສ່ວນສູງເປັນແມັດ

    Returns:
        float: ຄ່າ BMI
    """
    return weight / (height ** 2)

# ເບິ່ງ docstring
print(calculate_bmi.__doc__)
```

## Scope (ຂອບເຂດຂອງຕົວແປ)

```python
# Global variable
global_var = "ເປັນ global"

def test_scope():
    # Local variable
    local_var = "ເປັນ local"
    print(global_var)  # ເຂົ້າເຖິງ global ໄດ້
    print(local_var)

test_scope()
# print(local_var)  # Error! local_var ບໍ່ມີຢູ່ນອກ function

# ການໃຊ້ global keyword
count = 0

def increment():
    global count
    count += 1

increment()
print(count)  # 1
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

## ແບບຝຶກຫັດ

ລອງຂຽນ functions ເຫຼົ່ານີ້:

```python
# 1. Function ກວດສອບວ່າເປັນເລກຄູ່ຫຼືເລກຄີ່
def is_even(number):
    return number % 2 == 0

print(is_even(4))   # True
print(is_even(7))   # False

# 2. Function ຄົ້ນຫາເລກທີ່ໃຫຍ່ທີ່ສຸດ
def find_max(*numbers):
    if not numbers:
        return None
    max_num = numbers[0]
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num

print(find_max(3, 7, 2, 9, 1))  # 9

# 3. Function ກັບຄືນ string
def reverse_string(text):
    return text[::-1]

print(reverse_string("ສະບາຍດີ"))  # ີດາຍບະສ

# 4. Calculator function
def calculator(a, b, operation):
    operations = {
        'add': a + b,
        'subtract': a - b,
        'multiply': a * b,
        'divide': a / b if b != 0 else "ບໍ່ສາມາດຫານດ້ວຍ 0"
    }
    return operations.get(operation, "Operation ບໍ່ຖືກຕ້ອງ")

print(calculator(10, 5, 'add'))       # 15
print(calculator(10, 5, 'multiply'))  # 50
```

## Best Practices

1. **ໃຊ້ຊື່ທີ່ມີຄວາມໝາຍ**: `calculate_total()` ດີກວ່າ `calc()`
2. **Function ຄວນເຮັດພຽງແຕ່ສິ່ງດຽວ**
3. **ໃຊ້ docstrings ເພື່ອອະທິບາຍ function**
4. **Keep functions ສັ້ນ ແລະ ງ່າຍຕໍ່ການເຂົ້າໃຈ**
5. **ຫຼີກລ້ຽງການໃຊ້ global variables**

## ສະຫຼຸບ

ໃນບົດຮຽນນີ້ເຮົາໄດ້ຮຽນຮູ້:
- ການສ້າງ functions
- Parameters ແລະ return values
- Default parameters ແລະ keyword arguments
- *args ແລະ **kwargs
- Lambda functions
- Scope ແລະ recursive functions

Functions ແມ່ນພື້ນຖານສຳຄັນຂອງ Python programming. ຝຶກໃຊ້ເລື້ອຍໆເພື່ອໃຫ້ຊຳນານ!
"""
    },
    {
        'title': 'Object-Oriented Programming ໃນ Python',
        'slug': 'python-oop-lao',
        'category_name': 'Python',
        'difficulty': 'intermediate',
        'chapter': 2,
        'section': 1,
        'description': 'ຮຽນຮູ້ການຂຽນໂປຣແກຣມແບບ Object-Oriented ດ້ວຍ Classes ແລະ Objects',
        'content': """# Object-Oriented Programming ໃນ Python

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

## Class Variables vs Instance Variables

```python
class Student:
    # Class variable (ແບ່ງປັນໂດຍທຸກ instance)
    school_name = "ໂຮງຮຽນວຽງຈັນ"
    student_count = 0

    def __init__(self, name, grade):
        # Instance variables (ເປັນເອກະລັກຂອງແຕ່ລະ instance)
        self.name = name
        self.grade = grade
        Student.student_count += 1

    @classmethod
    def get_student_count(cls):
        return cls.student_count

# ສ້າງ students
student1 = Student("ສົມໃຈ", 10)
student2 = Student("ສົມຈິດ", 11)

print(Student.school_name)          # ໂຮງຮຽນວຽງຈັນ
print(Student.get_student_count())  # 2
```

## Methods (ວິທີການ)

### Instance Methods

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        """ຝາກເງິນ"""
        if amount > 0:
            self.balance += amount
            print(f"ຝາກ {amount:,.0f} ກີບ. ຍອດເງິນ: {self.balance:,.0f} ກີບ")
        else:
            print("ຈຳນວນເງິນຕ້ອງຫຼາຍກວ່າ 0")

    def withdraw(self, amount):
        """ຖອນເງິນ"""
        if amount > self.balance:
            print("ເງິນບໍ່ພໍ!")
        elif amount <= 0:
            print("ຈຳນວນເງິນຕ້ອງຫຼາຍກວ່າ 0")
        else:
            self.balance -= amount
            print(f"ຖອນ {amount:,.0f} ກີບ. ຍອດເງິນ: {self.balance:,.0f} ກີບ")

    def get_balance(self):
        """ເບິ່ງຍອດເງິນ"""
        return f"ຍອດເງິນຂອງ {self.owner}: {self.balance:,.0f} ກີບ"

# ໃຊ້ງານ
account = BankAccount("ສົມໃຈ", 1000000)
print(account.get_balance())
account.deposit(500000)
account.withdraw(300000)
```

### Class Methods

```python
class Date:
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    @classmethod
    def from_string(cls, date_string):
        """ສ້າງ Date ຈາກ string"""
        day, month, year = map(int, date_string.split('-'))
        return cls(day, month, year)

    def display(self):
        print(f"{self.day}/{self.month}/{self.year}")

# ໃຊ້ງານ
date1 = Date(1, 1, 2024)
date2 = Date.from_string("15-12-2024")

date1.display()  # 1/1/2024
date2.display()  # 15/12/2024
```

### Static Methods

```python
class MathHelper:
    @staticmethod
    def is_even(number):
        return number % 2 == 0

    @staticmethod
    def factorial(n):
        if n == 0 or n == 1:
            return 1
        return n * MathHelper.factorial(n-1)

# ໃຊ້ງານ (ບໍ່ຕ້ອງສ້າງ object)
print(MathHelper.is_even(10))     # True
print(MathHelper.factorial(5))    # 120
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

## Magic Methods (ວິທີການພິເສດ)

```python
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def __str__(self):
        """ເອີ້ນໃຊ້ເມື່ອ print"""
        return f"{self.title} ໂດຍ {self.author}"

    def __len__(self):
        """ເອີ້ນໃຊ້ເມື່ອ len()"""
        return self.pages

    def __lt__(self, other):
        """ເອີ້ນໃຊ້ເມື່ອປຽບທຽບ <"""
        return self.pages < other.pages

book1 = Book("ປະຫວັດສາດລາວ", "ຜູ້ຂຽນ A", 200)
book2 = Book("ວັດທະນະທຳລາວ", "ຜູ້ຂຽນ B", 150)

print(book1)           # ປະຫວັດສາດລາວ ໂດຍ ຜູ້ຂຽນ A
print(len(book1))      # 200
print(book2 < book1)   # True (150 < 200)
```

## ແບບຝຶກຫັດ

ລອງສ້າງ class ເຫຼົ່ານີ້:

```python
# 1. Library System
class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        print(f"ເພີ່ມໜັງສື: {book}")

    def list_books(self):
        print("\\n=== ລາຍການໜັງສືໃນຫ້ອງສະໝຸດ ===")
        for i, book in enumerate(self.books, 1):
            print(f"{i}. {book}")

# 2. Student Management
class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        self.grades = []

    def add_grade(self, grade):
        self.grades.append(grade)

    def average_grade(self):
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)

    def display_info(self):
        avg = self.average_grade()
        print(f"ນັກຮຽນ: {self.name}")
        print(f"ລະຫັດ: {self.student_id}")
        print(f"ຄະແນນສະເລ່ຍ: {avg:.2f}")
```

## ສະຫຼຸບ

OOP ໃນ Python ປະກອບດ້ວຍແນວຄິດສຳຄັນ:
- **Classes and Objects**: ການສ້າງແມ່ແບບ ແລະ instances
- **Inheritance**: ການສືບທອດຄຸນສົມບັດ
- **Encapsulation**: ການປົກປິດຂໍ້ມູນ
- **Polymorphism**: ການໃຊ້ງານແບບຫຼາກຫຼາຍ

OOP ຊ່ວຍໃຫ້ code ມີໂຄງສ້າງທີ່ດີ, ງ່າຍຕໍ່ການບຳລຸງຮັກສາ ແລະ ຂະຫຍາຍໄດ້!
"""
    },
]

def create_lao_docs():
    """Create Lao documentation"""
    print("=" * 80)
    print("📚 CREATING LAO LANGUAGE DOCUMENTATION")
    print("=" * 80)

    try:
        admin_user = User.objects.get(username='admin')
    except User.DoesNotExist:
        print("❌ Error: Admin user not found!")
        return

    created_count = 0

    for doc_data in DOCS:
        # Get or create category
        category, _ = Category.objects.get_or_create(
            slug=doc_data['category_name'].lower(),
            defaults={'name': doc_data['category_name']}
        )

        # Check if doc exists
        if Documentation.objects.filter(slug=doc_data['slug']).exists():
            print(f"⚠️  Skipping '{doc_data['title']}' - already exists")
            continue

        # Create documentation
        doc = Documentation.objects.create(
            title=doc_data['title'],
            slug=doc_data['slug'],
            author=admin_user,
            category=category,
            description=doc_data['description'],
            content=doc_data['content'],
            difficulty_level=doc_data['difficulty'],
            chapter_number=doc_data['chapter'],
            section_number=doc_data['section'],
            status='published',
            is_published=True
        )

        print(f"✅ Created: {doc_data['title']}")
        created_count += 1

    print("\n" + "=" * 80)
    print(f"📊 SUMMARY: Created {created_count} new documentation pages")
    print("=" * 80)
    print(f"\n🌐 View documentation at: http://127.0.0.1:8000/docs/")

if __name__ == '__main__':
    create_lao_docs()
