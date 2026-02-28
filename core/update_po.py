import os
import polib

locales_dir = 'locale'
languages = {
    'en': {
        'Lao': 'Lao',
        'Thai': 'Thai',
        'English': 'English',
        'Chinese': 'Chinese',
        'Blog': 'Blog',
        'Community': 'Community',
        'Courses': 'Courses',
        'Docs': 'Docs',
        'Events': 'Events',
        'ຄົ້ນຫາ...': 'Search...',
        'ສ້າງບົດຄວາມ': 'Create Post',
        'ອອກ': 'Log Out',
        'ເຂົ້າສູ່ລະບົບ': 'Log In',
        'ລົງທະບຽນ': 'Sign Up',
    },
    'th': {
        'Lao': 'ลาว',
        'Thai': 'ไทย',
        'English': 'อังกฤษ',
        'Chinese': 'จีน',
        'Blog': 'บล็อก',
        'Community': 'ชุมชน',
        'Courses': 'คอร์สเรียน',
        'Docs': 'เอกสารประกอบ',
        'Events': 'กิจกรรม',
        'ຄົ້ນຫາ...': 'ค้นหา...',
        'ສ້າງບົດຄວາມ': 'สร้างบทความ',
        'ອອກ': 'ออกจากระบบ',
        'ເຂົ້າສູ່ລະບົບ': 'เข้าสู่ระบบ',
        'ລົງທະບຽນ': 'ลงทะเบียน',
    },
    'zh_Hans': {
        'Lao': '老挝语',
        'Thai': '泰语',
        'English': '英语',
        'Chinese': '中文',
        'Blog': '博客',
        'Community': '社区',
        'Courses': '课程',
        'Docs': '文档',
        'Events': '活动',
        'ຄົ້ນຫາ...': '搜索...',
        'ສ້າງບົດຄວາມ': '创建文章',
        'ອອກ': '退出',
        'ເຂົ້າສູ່ລະບົບ': '登录',
        'ລົງທະບຽນ': '注册',
    },
    'lo': {
        'Lao': 'ລາວ',
        'Thai': 'ໄທ',
        'English': 'ອັງກິດ',
        'Chinese': 'ຈີນ',
        'Blog': 'ບົດຄວາມ',
        'Community': 'ຊຸມຊົນ',
        'Courses': 'ຄອສຮຽນ',
        'Docs': 'ເອກະສານ',
        'Events': 'ກິດຈະກຳ',
        'ຄົ້ນຫາ...': 'ຄົ້ນຫາ...',
        'ສ້າງບົດຄວາມ': 'ສ້າງບົດຄວາມ',
        'ອອກ': 'ອອກຈາກລະບົບ',
        'ເຂົ້າສູ່ລະບົບ': 'ເຂົ້າສູ່ລະບົບ',
        'ລົງທະບຽນ': 'ລົງທະບຽນ',
    }
}

for lang, trans_dict in languages.items():
    po_path = os.path.join(locales_dir, lang, 'LC_MESSAGES', 'django.po')
    if os.path.exists(po_path):
        po = polib.pofile(po_path)
        for entry in po:
            if entry.msgid in trans_dict:
                entry.msgstr = trans_dict[entry.msgid]
        po.save(po_path)
        print(f"Updated {lang} translations.")
    else:
        print(f"File not found: {po_path}")
