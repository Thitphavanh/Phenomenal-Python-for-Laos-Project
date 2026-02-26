"""
Script to create Python installation documentation in Lao language
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

# Get Python category
python_cat, created = Category.objects.get_or_create(
    slug='python',
    defaults={'name': 'Python', 'description': 'Python programming tutorials'}
)

# Lao language Python installation guide
lao_python_install = {
    'title': 'ວິທີການຕິດຕັ້ງ Python ສຳລັບຜູ້ເລີ່ມຕົ້ນ',
    'slug': 'lao-python-installation-guide',
    'category': python_cat,
    'difficulty_level': 'beginner',
    'doc_order': 0,
    'excerpt': 'ຄູ່ມືການຕິດຕັ້ງ Python ແບບລະອຽດສຳລັບລະບົບປະຕິບັດການທັງໝົດ ລວມທັງ Windows, macOS ແລະ Linux',
    'content': '''## ພາສາ Python ແມ່ນຫຍັງ?

Python ແມ່ນພາສາໂປຣແກຣມທີ່ມີລະດັບສູງ, ງ່າຍຕໍ່ການຮຽນຮູ້ ແລະ ມີປະສິດທິພາບສູງ. ມັນຖືກໃຊ້ຢ່າງກວ້າງຂວາງໃນການພັດທະນາເວັບໄຊທ์, ວິທະຍາສາດຂໍ້ມູນ, ປັນຍາປະດິດ, ແລະອື່ນໆອີກຫຼາຍ.

## ເປັນຫຍັງຄວນຮຽນ Python?

Python ເປັນພາສາທີ່ດີທີ່ສຸດສຳລັບຜູ້ເລີ່ມຕົ້ນເພາະວ່າ:

- **ງ່າຍຕໍ່ການຮຽນຮູ້**: ໄວຍະກອນທີ່ຊັດເຈນ ແລະ ອ່ານງ່າຍ
- **ຊຸມຊົນໃຫຍ່**: ມີຄົນຫຼາຍລ້ານຄົນໃນທົ່ວໂລກທີ່ໃຊ້ Python
- **ຫຼາກຫຼາຍການນຳໃຊ້**: ສາມາດໃຊ້ໄດ້ໃນງານຫຼາຍປະເພດ
- **ຕ້ອງການສູງ**: ວຽກງານ Python Developer ມີຄວາມຕ້ອງການສູງ
- **ຟຣີ ແລະ Open Source**: ບໍ່ຕ້ອງເສຍຄ່າໃຊ້ຈ່າຍ

## ກ່ອນທີ່ຈະເລີ່ມຕົ້ນ

ກ່ອນທີ່ຈະຕິດຕັ້ງ Python, ທ່ານຄວນ:

1. ເລືອກລະບົບປະຕິບັດການທີ່ທ່ານໃຊ້ (Windows, macOS, ຫຼື Linux)
2. ກວດສອບວ່າຄອມພິວເຕີຂອງທ່ານມີພື້ນທີ່ເພີ່ມພໍ (ປະມານ 100 MB)
3. ມີການເຊື່ອມຕໍ່ອິນເຕີເນັດສຳລັບດາວໂຫຼດ

## ການຕິດຕັ້ງ Python ເທິງ Windows

### ວິທີທີ 1: ດາວໂຫຼດຈາກເວັບໄຊທ์ທາງການ

#### ຂັ້ນຕອນທີ 1: ດາວໂຫຼດໂປຣແກຣມຕິດຕັ້ງ

1. ເປີດບຣາວເຊີຂອງທ່ານ ແລະ ໄປທີ່ [python.org/downloads](https://www.python.org/downloads/)
2. ເວັບໄຊທ์ຈະຕັດສິນໃຈອັດຕະໂນມັດວ່າທ່ານກຳລັງໃຊ້ Windows
3. ກົດປຸ່ມ "Download Python 3.12.x" (ເລກເວີຊັນອາດຈະແຕກຕ່າງກັນ)
4. ລໍຖ້າໄຟລ์ດາວໂຫຼດສຳເລັດ (ປະມານ 25-30 MB)

#### ຂັ້ນຕອນທີ 2: ຕິດຕັ້ງ Python

1. ຊອກຫາໄຟລ์ທີ່ດາວໂຫຼດມາ (ປົກກະຕິຢູ່ໃນໂຟນເດີ Downloads)
2. ດັບເບີນຄລິກໃສ່ໄຟລ์ `python-3.12.x.exe` ເພື່ອເປີດໂປຣແກຣມຕິດຕັ້ງ
3. **ສຳຄັນຫຼາຍ**: ໃຫ້ກົດຕິກໃສ່ "Add Python to PATH" ກ່ອນ!
4. ກົດປຸ່ມ "Install Now"
5. ລໍຖ້າການຕິດຕັ້ງສຳເລັດ (ປະມານ 2-3 ນາທີ)
6. ກົດ "Close" ເມື່ອເສັດແລ້ວ

#### ຂັ້ນຕອນທີ 3: ກວດສອບການຕິດຕັ້ງ

1. ກົດ `Win + R` ແລະ ພິມ `cmd` ແລ້ວກົດ Enter
2. ໃນ Command Prompt, ພິມຄຳສັ່ງຕໍ່ໄປນີ້:

```bash
python --version
```

3. ຖ້າຕິດຕັ້ງສຳເລັດ, ມັນຈະສະແດງເລກເວີຊັນຂອງ Python:

```bash
Python 3.12.0
```

### ວິທີທີ 2: ໃຊ້ Microsoft Store (ແນະນຳສຳລັບ Windows 10/11)

1. ເປີດ Microsoft Store
2. ຄົ້ນຫາ "Python 3.12"
3. ກົດປຸ່ມ "Get" ຫຼື "Install"
4. ລໍຖ້າການດາວໂຫຼດ ແລະ ຕິດຕັ້ງສຳເລັດ

**ຂໍ້ດີ**: ງ່າຍກວ່າ, ອັບເດດອັດຕະໂນມັດ
**ຂໍ້ເສຍ**: ບາງຄັ້ງມີຂໍ້ຈຳກັດໃນການໃຊ້ງານບາງຢ່າງ

## ການຕິດຕັ້ງ Python ເທິງ macOS

### ວິທີທີ 1: ໃຊ້ Homebrew (ແນະນຳ)

Homebrew ແມ່ນເຄື່ອງມືຈັດການ package ທີ່ນິຍົມໃຊ້ໃນ macOS.

#### ຂັ້ນຕອນທີ 1: ຕິດຕັ້ງ Homebrew (ຖ້າຍັງບໍ່ມີ)

1. ເປີດ Terminal (Command + Space, ແລ້ວພິມ "Terminal")
2. ວາງ ແລະ ກົດ Enter:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

3. ລໍຖ້າການຕິດຕັ້ງສຳເລັດ (ອາດໃຊ້ເວລາ 5-10 ນາທີ)

#### ຂັ້ນຕອນທີ 2: ຕິດຕັ້ງ Python ດ້ວຍ Homebrew

```bash
brew install python3
```

#### ຂັ້ນຕອນທີ 3: ກວດສອບການຕິດຕັ້ງ

```bash
python3 --version
```

### ວິທີທີ 2: ດາວໂຫຼດຈາກເວັບໄຊທ์ທາງການ

1. ໄປທີ່ [python.org/downloads/macos](https://www.python.org/downloads/macos/)
2. ດາວໂຫຼດໄຟລ์ `.pkg` ເວີຊັນຫຼ້າສຸດ
3. ເປີດໄຟລ์ທີ່ດາວໂຫຼດມາ
4. ປະຕິບັດຕາມຂັ້ນຕອນການຕິດຕັ້ງ
5. ກົດ "Install" ແລະ ໃສ່ລະຫັດຜ່ານຂອງທ່ານເມື່ອມີການຮ້ອງຂໍ

## ການຕິດຕັ້ງ Python ເທິງ Linux

ສ່ວນຫຼາຍຂອງລະບົບ Linux ມີ Python ຕິດຕັ້ງມາແລ້ວ, ແຕ່ອາດຈະເປັນເວີຊັນເກົ່າ.

### Ubuntu/Debian

#### ກວດສອບເວີຊັນປັດຈຸບັນ:

```bash
python3 --version
```

#### ຕິດຕັ້ງເວີຊັນຫຼ້າສຸດ:

```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Fedora/CentOS/RHEL

```bash
sudo dnf install python3 python3-pip
```

### Arch Linux

```bash
sudo pacman -S python python-pip
```

## ຕິດຕັ້ງ pip (Python Package Manager)

pip ແມ່ນເຄື່ອງມືສຳລັບຕິດຕັ້ງແພັກເກັດ Python. ໃນເວີຊັນ Python 3.4+ pip ຖືກຕິດຕັ້ງມາພ້ອມກັບ Python ແລ້ວ.

### ກວດສອບວ່າມີ pip ຫຼືບໍ່:

```bash
pip --version
```

ຫຼື

```bash
pip3 --version
```

### ຖ້າບໍ່ມີ pip, ຕິດຕັ້ງດ້ວຍຄຳສັ່ງ:

**Windows:**
```bash
python -m ensurepip --upgrade
```

**macOS/Linux:**
```bash
python3 -m ensurepip --upgrade
```

## ການຕັ້ງຄ່າ Environment (ສະພາບແວດລ້ອມ)

### ການສ້າງ Virtual Environment

Virtual Environment ຊ່ວຍໃຫ້ທ່ານແຍກ dependencies ຂອງໂປຣເຈັກແຕ່ລະໂປຣເຈັກ.

#### Windows:

```bash
# ສ້າງ virtual environment
python -m venv myenv

# ເປີດໃຊ້ງານ
myenv\Scripts\activate
```

#### macOS/Linux:

```bash
# ສ້າງ virtual environment
python3 -m venv myenv

# ເປີດໃຊ້ງານ
source myenv/bin/activate
```

#### ປິດການໃຊ້ງານ Virtual Environment:

```bash
deactivate
```

## ການຕິດຕັ້ງ IDE (Integrated Development Environment)

### 1. Visual Studio Code (ແນະນຳ)

**ເປັນຫຍັງຖືກເລືອກ?**
- ຟຣີ ແລະ Open Source
- ມີ extension ສຳລັບ Python ທີ່ດີຫຼາຍ
- ມີນ້ຳໜັກເບົາ
- ໃຊ້ງ່າຍ

**ວິທີຕິດຕັ້ງ:**
1. ໄປທີ່ [code.visualstudio.com](https://code.visualstudio.com/)
2. ດາວໂຫຼດເວີຊັນສຳລັບລະບົບປະຕິບັດການຂອງທ່ານ
3. ຕິດຕັ້ງຕາມປົກກະຕິ
4. ເປີດ VS Code ແລະ ຕິດຕັ້ງ Python extension:
   - ກົດ Ctrl+Shift+X (Windows/Linux) ຫຼື Cmd+Shift+X (macOS)
   - ຄົ້ນຫາ "Python"
   - ຕິດຕັ້ງ extension ທີ່ພັດທະນາໂດຍ Microsoft

### 2. PyCharm Community Edition

**ເປັນຫຍັງຖືກເລືອກ?**
- IDE ທີ່ເຕັມຮູບແບບສະເພາະສຳລັບ Python
- ມີເຄື່ອງມື debug ທີ່ເຂັ້ມແຂງ
- Community Edition ແມ່ນຟຣີ

**ວິທີຕິດຕັ້ງ:**
1. ໄປທີ່ [jetbrains.com/pycharm/download](https://www.jetbrains.com/pycharm/download/)
2. ດາວໂຫຼດ Community Edition (ຟຣີ)
3. ຕິດຕັ້ງຕາມຄຳແນະນຳ

### 3. Jupyter Notebook (ສຳລັບ Data Science)

**ວິທີຕິດຕັ້ງ:**

```bash
pip install jupyter
```

**ວິທີເປີດໃຊ້:**

```bash
jupyter notebook
```

## ທົດສອບການຕິດຕັ້ງ

### ສ້າງໂປຣແກຣມ Python ທຳອິດຂອງທ່ານ

1. ເປີດ text editor ຫຼື IDE
2. ສ້າງໄຟລ์ໃໝ່ຊື່ວ່າ `hello.py`
3. ພິມໂຄດຕໍ່ໄປນີ້:

```python
print("ສະບາຍດີ, Python!")
print("ຂ້ອຍກຳລັງຮຽນ Python")

# ຄິດໄລ່ການບວກ
a = 5
b = 3
ຜົນບວກ = a + b
print(f"{a} + {b} = {ຜົນບວກ}")
```

4. ບັນທຶກໄຟລ์
5. ເປີດ Terminal/Command Prompt ໃນໂຟນເດີຂອງໄຟລ์
6. ແລ່ນໂປຣແກຣມ:

```bash
python hello.py
```

**ຜົນລັບທີ່ຄາດວ່າຈະໄດ້ຮັບ:**
```
ສະບາຍດີ, Python!
ຂ້ອຍກຳລັງຮຽນ Python
5 + 3 = 8
```

## ການແກ້ໄຂບັນຫາທົ່ວໄປ

### ບັນຫາ: "python is not recognized" ເທິງ Windows

**ວິທີແກ້ໄຂ:**
1. ກັບໄປຕິດຕັ້ງໃໝ່ ແລະ ຢ່າລືມກົດຕິກ "Add Python to PATH"
2. ຫຼື ເພີ່ມ PATH ດ້ວຍຕົນເອງ:
   - ຄລິກຂວາທີ່ "This PC" → Properties
   - Advanced system settings → Environment Variables
   - ເພີ່ມ path ຂອງ Python (ປົກກະຕິ: `C:\Users\YourName\AppData\Local\Programs\Python\Python312`)

### ບັນຫາ: Permission denied ເທິງ macOS/Linux

**ວິທີແກ້ໄຂ:**
ໃຊ້ `python3` ແທນ `python`:

```bash
python3 hello.py
```

### ບັນຫາ: pip ຕິດຕັ້ງບໍ່ໄດ້

**ວິທີແກ້ໄຂ:**

```bash
# Windows
python -m pip install --upgrade pip

# macOS/Linux
python3 -m pip install --upgrade pip
```

## ແພັກເກັດທີ່ແນະນຳສຳລັບຜູ້ເລີ່ມຕົ້ນ

ຕິດຕັ້ງແພັກເກັດເຫຼົ່ານີ້ເພື່ອເລີ່ມຕົ້ນ:

```bash
# ສຳລັບການວິເຄາະຂໍ້ມູນ
pip install numpy pandas matplotlib

# ສຳລັບການພັດທະນາເວັບ
pip install django flask

# ສຳລັບການຮຽນຮູ້ເຄື່ອງຈັກ
pip install scikit-learn tensorflow

# ເຄື່ອງມືທົ່ວໄປທີ່ມີປະໂຫຍດ
pip install requests beautifulsoup4
```

## ຂັ້ນຕອນຕໍ່ໄປ

ຫຼັງຈາກຕິດຕັ້ງ Python ແລ້ວ, ທ່ານຄວນ:

1. **ຮຽນພື້ນຖານຂອງ Python**
   - ຕົວແປ (Variables)
   - ປະເພດຂໍ້ມູນ (Data Types)
   - ການຄວບຄຸມການໄຫຼ (Control Flow)
   - ຟັງຊັນ (Functions)
   - ຄລາສ (Classes)

2. **ເຮັດໂປຣເຈັກຂະໜາດນ້ອຍ**
   - ເຄື່ອງຄິດເລກ
   - ເກມຕີ ລາຍ
   - ໂປຣແກຣມຄຸ້ມຄອງລາຍການ To-Do

3. **ເຂົ້າຮ່ວມຊຸມຊົນ**
   - Stack Overflow
   - Reddit r/learnpython
   - Python Discord servers
   - ກຸ່ມ Python ໃນລາວ

4. **ອ່ານເອກະສານທາງການ**
   - [Python Official Tutorial](https://docs.python.org/3/tutorial/)
   - [Real Python](https://realpython.com/)
   - [Python for Laos Documentation](/)

## ຄຳແນະນຳສຳລັບການຮຽນຮູ້

1. **ຝຶກເປັນປະຈຳ**: ພະຍາຍາມຂຽນໂຄດທຸກມື້ ແມ່ນແຕ່ພຽງ 15-30 ນາທີ
2. **ສ້າງໂປຣເຈັກ**: ການຮຽນຮູ້ຜ່ານການປະຕິບັດແມ່ນວິທີທີ່ດີທີ່ສຸດ
3. **ອ່ານໂຄດຄົນອື່ນ**: ເບິ່ງວ່າຄົນອື່ນແກ້ບັນຫາແນວໃດ
4. **ຢ່າຢ້ານຄວາມຜິດພາດ**: Error messages ແມ່ນໂອກາດໃນການຮຽນຮູ້
5. **ຮ່ວມມືກັບຊຸມຊົນ**: ຖາມຄຳຖາມ ແລະ ຊ່ວຍເຫຼືອຄົນອື່ນ

## ແຫຼ່ງຮຽນຮູ້ທີ່ແນະນຳ

### ພາສາອັງກິດ
- **ເວັບໄຊທ์**: Real Python, Python.org, W3Schools
- **YouTube**: Corey Schafer, Tech With Tim, Programming with Mosh
- **ຫນັງສື**: "Python Crash Course" by Eric Matthes
- **ອອນລາຍ**: Coursera, edX, Udemy

### ພາສາລາວ/ໄທ
- **PythonForLaos**: ເອກະສານແລະບົດຮຽນເປັນພາສາລາວ
- **YouTube ໄທ**: Uncle Engineer, CodeBangkok
- **Facebook Groups**: Python Learners Laos, Python Thailand

## ສະຫຼຸບ

ການຕິດຕັ້ງ Python ແມ່ນຂັ້ນຕອນທຳອິດທີ່ສຳຄັນໃນການເລີ່ມຕົ້ນເສັ້ນທາງການຂຽນໂປຣແກຣມຂອງທ່ານ. ຢ່າລືມ:

✅ ເລືອກວິທີການຕິດຕັ້ງທີ່ເໝາະສົມກັບລະບົບປະຕິບັດການຂອງທ່ານ
✅ ກວດສອບການຕິດຕັ້ງດ້ວຍຄຳສັ່ງ `python --version`
✅ ຕິດຕັ້ງ IDE ທີ່ເໝາະສົມ
✅ ສ້າງ ແລະ ແລ່ນໂປຣແກຣມທຳອິດຂອງທ່ານ
✅ ເລີ່ມຮຽນພື້ນຖານຂອງ Python

ໂຊກດີໃນການຮຽນຮູ້! 🐍🇱🇦

## ຕິດຕໍ່ ແລະ ຊ່ວຍເຫຼືອ

ຖ້າທ່ານມີຄຳຖາມ ຫຼື ຕ້ອງການຄວາມຊ່ວຍເຫຼືອ:

- 📧 Email: support@pythonforlaos.com
- 💬 Facebook: Python for Laos Community
- 🐦 Twitter: @PythonForLaos
- 📚 Documentation: [pythonforlaos.com/docs](/docs/)

---

**ສ້າງໂດຍ**: Python for Laos Team
**ອັບເດດລ່າສຸດ**: ທັນວາ 2025
**ລິຂະສິດ**: © 2025 Python for Laos. All rights reserved.
''',
}

# Create or update the documentation post
post, created = Post.objects.update_or_create(
    slug=lao_python_install['slug'],
    defaults={
        'title': lao_python_install['title'],
        'author': admin_user,
        'category': lao_python_install['category'],
        'content': lao_python_install['content'],
        'excerpt': lao_python_install['excerpt'],
        'post_type': 'doc',
        'difficulty_level': lao_python_install['difficulty_level'],
        'doc_order': lao_python_install['doc_order'],
        'status': 'published',
    }
)

action = "ສ້າງ" if created else "ອັບເດດ"
print(f"{action} ເອກະສານສຳເລັດ: {post.title}")
print(f"URL: /docs/{post.slug}/")
print(f"\nທ່ານສາມາດເບິ່ງເອກະສານໄດ້ທີ່: http://127.0.0.1:8000/docs/{post.slug}/")
