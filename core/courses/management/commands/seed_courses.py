"""
Management command to seed sample course data
Usage: python manage.py seed_courses
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from courses.models import Course, CourseChapter, Lesson
from blog.models import Category, Tag


class Command(BaseCommand):
    help = 'Seed sample course data for Python for Laos'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting to seed course data...'))

        # Get or create instructor
        instructor, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@pythonforlaos.com',
                'first_name': 'Python',
                'last_name': 'Instructor',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            instructor.set_password('admin123')
            instructor.save()
            self.stdout.write(self.style.SUCCESS(f'Created instructor: {instructor.username}'))
        else:
            self.stdout.write(self.style.WARNING(f'Instructor already exists: {instructor.username}'))

        # Get or create categories
        python_cat, _ = Category.objects.get_or_create(
            slug='python',
            defaults={
                'name': 'Python Programming',
                'description': 'Learn Python programming from scratch'
            }
        )

        web_cat, _ = Category.objects.get_or_create(
            slug='web-development',
            defaults={
                'name': 'Web Development',
                'description': 'Web development courses'
            }
        )

        data_cat, _ = Category.objects.get_or_create(
            slug='data-science',
            defaults={
                'name': 'Data Science',
                'description': 'Data science and analytics'
            }
        )

        # Get or create tags
        beginner_tag, _ = Tag.objects.get_or_create(
            slug='beginner',
            defaults={'name': 'Beginner'}
        )
        python_tag, _ = Tag.objects.get_or_create(
            slug='python',
            defaults={'name': 'Python'}
        )
        django_tag, _ = Tag.objects.get_or_create(
            slug='django',
            defaults={'name': 'Django'}
        )
        data_tag, _ = Tag.objects.get_or_create(
            slug='data-analysis',
            defaults={'name': 'Data Analysis'}
        )

        # Course 1: Python Basics
        course1_slug = 'python-basics-for-beginners'
        course1, created = Course.objects.get_or_create(
            slug=course1_slug,
            defaults={
                'title': 'Python ພື້ນຖານສຳລັບຜູ້ເລີ່ມຕົ້ນ',
                'instructor': instructor,
                'short_description': 'ຮຽນ Python ຈາກພື້ນຖານຈົນເຖິງການຂຽນໂປແກມທີ່ເຂັ້ມແຂງ',
                'description': '''
                    <h2>ກ່ຽວກັບຄອດສຶກສານີ້</h2>
                    <p>ຄອດສຶກສານີ້ຈະສອນທ່ານ Python ຈາກພື້ນຖານຈົນສາມາດຂຽນໂປແກມໄດ້ດ້ວຍຕົນເອງ</p>

                    <h3>ທ່ານຈະໄດ້ຮຽນຮູ້:</h3>
                    <ul>
                        <li>ພື້ນຖານການຂຽນໂປແກມດ້ວຍ Python</li>
                        <li>ຕົວແປ, ຊະນິດຂໍ້ມູນ, ແລະ operators</li>
                        <li>Control flow (if/else, loops)</li>
                        <li>Functions ແລະ modules</li>
                        <li>Working with files</li>
                        <li>Object-Oriented Programming ພື້ນຖານ</li>
                    </ul>
                ''',
                'category': python_cat,
                'difficulty': 'beginner',
                'is_free': True,
                'price': 0,
                'duration_hours': 10,
                'total_lessons': 0,
                'total_students': 1250,
                'learning_objectives': '''ເຂົ້າໃຈພື້ນຖານການຂຽນໂປແກມ Python
ສາມາດຂຽນໂປແກມ Python ງ່າຍໆໄດ້
ເຂົ້າໃຈ OOP ພື້ນຖານ
ສາມາດອ່ານແລະຂຽນໄຟລ໌ໄດ້
ສາມາດສ້າງ functions ແລະ modules ຂອງຕົນເອງໄດ້''',
                'prerequisites': '''ບໍ່ຕ້ອງມີປະສົບການກ່ອນໜ້ານີ້
ມີຄອມພິວເຕີທີ່ສາມາດຕິດຕັ້ງ Python ໄດ້
ມີຄວາມຕັ້ງໃຈຮຽນຮູ້''',
                'status': 'published',
                'is_featured': True,
            }
        )
        if created:
            course1.tags.add(beginner_tag, python_tag)
            self.stdout.write(self.style.SUCCESS(f'Created course: {course1.title}'))

            # Add chapters and lessons for course 1
            self._create_python_basics_content(course1)
        else:
            self.stdout.write(self.style.WARNING(f'Course already exists: {course1.title}'))

        # Course 2: Django Web Development
        course2_slug = 'django-web-development'
        course2, created = Course.objects.get_or_create(
            slug=course2_slug,
            defaults={
                'title': 'Django Web Development ສຳລັບຜູ້ເລີ່ມຕົ້ນ',
                'instructor': instructor,
                'short_description': 'ສ້າງເວັບແອັບພລິເຄຊັນດ້ວຍ Django Framework',
                'description': '''
                    <h2>ກ່ຽວກັບຄອດສຶກສານີ້</h2>
                    <p>ຮຽນຮູ້ການສ້າງເວັບແອັບພລິເຄຊັນດ້ວຍ Django - framework ຍອດນິຍົມຂອງ Python</p>

                    <h3>ທ່ານຈະໄດ້ຮຽນຮູ້:</h3>
                    <ul>
                        <li>ຕິດຕັ້ງແລະຕັ້ງຄ່າ Django</li>
                        <li>Models, Views, Templates (MVT)</li>
                        <li>URL routing ແລະ forms</li>
                        <li>User authentication</li>
                        <li>Database operations</li>
                        <li>Deploy Django app</li>
                    </ul>
                ''',
                'category': web_cat,
                'difficulty': 'intermediate',
                'is_free': False,
                'price': 299000,
                'duration_hours': 15,
                'total_lessons': 0,
                'total_students': 850,
                'learning_objectives': '''ສ້າງເວັບແອັບດ້ວຍ Django ໄດ້
ເຂົ້າໃຈ MVT architecture
ສາມາດເຮັດ CRUD operations
ສ້າງລະບົບ authentication
Deploy application ໄປ production''',
                'prerequisites': '''ມີຄວາມຮູ້ພື້ນຖານ Python
ເຂົ້າໃຈພື້ນຖານ HTML/CSS
ມີປະສົບການກັບ command line''',
                'status': 'published',
                'is_featured': True,
            }
        )
        if created:
            course2.tags.add(python_tag, django_tag)
            self.stdout.write(self.style.SUCCESS(f'Created course: {course2.title}'))

            # Add chapters and lessons for course 2
            self._create_django_content(course2)
        else:
            self.stdout.write(self.style.WARNING(f'Course already exists: {course2.title}'))

        # Course 3: Data Analysis with Python
        course3_slug = 'python-data-analysis'
        course3, created = Course.objects.get_or_create(
            slug=course3_slug,
            defaults={
                'title': 'Python ສຳລັບການວິເຄາະຂໍ້ມູນ',
                'instructor': instructor,
                'short_description': 'ຮຽນຮູ້ການວິເຄາະຂໍ້ມູນດ້ວຍ Pandas, NumPy ແລະ Matplotlib',
                'description': '''
                    <h2>ກ່ຽວກັບຄອດສຶກສານີ້</h2>
                    <p>ຮຽນການວິເຄາະແລະສ້າງຮູບພາບຂໍ້ມູນດ້ວຍ Python libraries ຍອດນິຍົມ</p>

                    <h3>ທ່ານຈະໄດ້ຮຽນຮູ້:</h3>
                    <ul>
                        <li>NumPy arrays ແລະ operations</li>
                        <li>Pandas DataFrames</li>
                        <li>Data cleaning ແລະ preprocessing</li>
                        <li>Data visualization ດ້ວຍ Matplotlib</li>
                        <li>Statistical analysis</li>
                        <li>Real-world data projects</li>
                    </ul>
                ''',
                'category': data_cat,
                'difficulty': 'intermediate',
                'is_free': False,
                'price': 399000,
                'duration_hours': 12,
                'total_lessons': 0,
                'total_students': 620,
                'learning_objectives': '''ເຂົ້າໃຈການໃຊ້ Pandas ແລະ NumPy
ສາມາດ clean ແລະ process ຂໍ້ມູນໄດ້
ສ້າງກຣາຟແລະການສະແດງຜົນຂໍ້ມູນ
ວິເຄາະຂໍ້ມູນສະຖິຕິພື້ນຖານ
ປະຕິບັດໂຄງການວິເຄາະຂໍ້ມູນຈິງ''',
                'prerequisites': '''ມີຄວາມຮູ້ Python ພື້ນຖານ
ເຂົ້າໃຈຄະນິດສາດພື້ນຖານ
ມີຄວາມສົນໃຈໃນການວິເຄາະຂໍ້ມູນ''',
                'status': 'published',
                'is_featured': False,
            }
        )
        if created:
            course3.tags.add(python_tag, data_tag)
            self.stdout.write(self.style.SUCCESS(f'Created course: {course3.title}'))

            # Add chapters and lessons for course 3
            self._create_data_analysis_content(course3)
        else:
            self.stdout.write(self.style.WARNING(f'Course already exists: {course3.title}'))

        # Course 4: Advanced Python
        course4_slug = 'advanced-python-programming'
        course4, created = Course.objects.get_or_create(
            slug=course4_slug,
            defaults={
                'title': 'Python ຂັ້ນສູງ - Advanced Concepts',
                'instructor': instructor,
                'short_description': 'ເຮັດຄວາມຮູ້ Python ຂອງທ່ານໃຫ້ເລິກເຊິ່ງຂຶ້ນ',
                'description': '''
                    <h2>ກ່ຽວກັບຄອດສຶກສານີ້</h2>
                    <p>ຮຽນຮູ້ຫົວຂໍ້ Python ຂັ້ນສູງເພື່ອກາຍເປັນ Python developer ທີ່ມີທັກສະສູງ</p>

                    <h3>ທ່ານຈະໄດ້ຮຽນຮູ້:</h3>
                    <ul>
                        <li>Decorators ແລະ context managers</li>
                        <li>Generators ແລະ iterators</li>
                        <li>Async/await programming</li>
                        <li>Testing ດ້ວຍ pytest</li>
                        <li>Design patterns</li>
                        <li>Performance optimization</li>
                    </ul>
                ''',
                'category': python_cat,
                'difficulty': 'advanced',
                'is_free': False,
                'price': 499000,
                'duration_hours': 18,
                'total_lessons': 0,
                'total_students': 380,
                'learning_objectives': '''ເຂົ້າໃຈ advanced Python concepts
ຂຽນ asynchronous code
ສ້າງ tests ທີ່ມີປະສິດທິພາບ
ນຳໃຊ້ design patterns
Optimize code performance''',
                'prerequisites': '''ມີປະສົບການ Python ຢ່າງໜ້ອຍ 6 ເດືອນ
ເຂົ້າໃຈ OOP ດີ
ມີໂຄງການ Python ທີ່ເຄີຍເຮັດມາແລ້ວ''',
                'status': 'published',
                'is_featured': False,
            }
        )
        if created:
            course4.tags.add(python_tag)
            self.stdout.write(self.style.SUCCESS(f'Created course: {course4.title}'))

            # Add chapters and lessons for course 4
            self._create_advanced_python_content(course4)
        else:
            self.stdout.write(self.style.WARNING(f'Course already exists: {course4.title}'))

        self.stdout.write(self.style.SUCCESS('\n✅ Course seeding completed successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Total courses: {Course.objects.count()}'))

    def _create_python_basics_content(self, course):
        """Create chapters and lessons for Python Basics course"""

        # Chapter 1
        chapter1 = CourseChapter.objects.create(
            course=course,
            title='ການແນະນຳ Python',
            description='ເລີ່ມຕົ້ນກັບ Python programming',
            order=1
        )

        Lesson.objects.create(
            course=course,
            chapter=chapter1,
            title='Python ຄືຫຍັງ?',
            slug='what-is-python',
            description='ແນະນຳພື້ນຖານກ່ຽວກັບ Python',
            content_type='video',
            video_url='https://www.youtube.com/embed/Y8Tko2YC5hA',
            content='<p>Python ເປັນພາສາໂປຼແກຼມທີ່ນິຍົມທີ່ສຸດໃນໂລກ...</p>',
            duration_minutes=15,
            order=1,
            is_preview=True
        )

        Lesson.objects.create(
            course=course,
            chapter=chapter1,
            title='ຕິດຕັ້ງ Python',
            slug='installing-python',
            description='ວິທີການຕິດຕັ້ງ Python ເທິງ Windows, Mac, Linux',
            content_type='video',
            video_url='https://www.youtube.com/embed/YYXdXT2l-Gg',
            content='<p>ຄູ່ມືການຕິດຕັ້ງ Python ລາຍລະອຽດ...</p>',
            duration_minutes=20,
            order=2,
            is_preview=True
        )

        # Chapter 2
        chapter2 = CourseChapter.objects.create(
            course=course,
            title='Python ພື້ນຖານ',
            description='ຮຽນຮູ້ພື້ນຖານຂອງ Python',
            order=2
        )

        Lesson.objects.create(
            course=course,
            chapter=chapter2,
            title='ຕົວແປແລະຊະນິດຂໍ້ມູນ',
            slug='variables-and-data-types',
            description='ເຂົ້າໃຈຕົວແປແລະຊະນິດຂໍ້ມູນໃນ Python',
            content_type='video',
            content='<p>ການສ້າງແລະໃຊ້ງານຕົວແປໃນ Python...</p>',
            duration_minutes=25,
            order=1
        )

        Lesson.objects.create(
            course=course,
            chapter=chapter2,
            title='Operators ໃນ Python',
            slug='python-operators',
            description='ຮຽນຮູ້ Arithmetic, Comparison, Logical operators',
            content_type='video',
            content='<p>Operators ຕ່າງໆທີ່ໃຊ້ໃນ Python...</p>',
            duration_minutes=20,
            order=2
        )

        # Update course total lessons
        course.update_total_lessons()
        course.update_duration()

    def _create_django_content(self, course):
        """Create chapters and lessons for Django course"""

        # Chapter 1
        chapter1 = CourseChapter.objects.create(
            course=course,
            title='Django ພື້ນຖານ',
            description='ເລີ່ມຕົ້ນກັບ Django framework',
            order=1
        )

        Lesson.objects.create(
            course=course,
            chapter=chapter1,
            title='Django ຄືຫຍັງ?',
            slug='what-is-django',
            description='ແນະນຳ Django web framework',
            content_type='video',
            content='<p>Django ເປັນ web framework ທີ່ມີພະລັງ...</p>',
            duration_minutes=18,
            order=1,
            is_preview=True
        )

        Lesson.objects.create(
            course=course,
            chapter=chapter1,
            title='ຕິດຕັ້ງ Django',
            slug='installing-django',
            description='Setup Django development environment',
            content_type='video',
            content='<p>ວິທີການຕິດຕັ້ງແລະຕັ້ງຄ່າ Django...</p>',
            duration_minutes=22,
            order=2
        )

        # Chapter 2
        chapter2 = CourseChapter.objects.create(
            course=course,
            title='Models ແລະ Database',
            description='ເຮັດວຽກກັບ Django models',
            order=2
        )

        Lesson.objects.create(
            course=course,
            chapter=chapter2,
            title='ສ້າງ Django Models',
            slug='creating-models',
            description='ວິທີການສ້າງແລະໃຊ້ງານ models',
            content_type='video',
            content='<p>Models ເປັນພື້ນຖານຂອງ Django...</p>',
            duration_minutes=30,
            order=1
        )

        course.update_total_lessons()
        course.update_duration()

    def _create_data_analysis_content(self, course):
        """Create chapters and lessons for Data Analysis course"""

        # Chapter 1
        chapter1 = CourseChapter.objects.create(
            course=course,
            title='NumPy ພື້ນຖານ',
            description='ເລີ່ມຕົ້ນກັບ NumPy library',
            order=1
        )

        Lesson.objects.create(
            course=course,
            chapter=chapter1,
            title='ແນະນຳ NumPy',
            slug='intro-to-numpy',
            description='NumPy arrays ແລະການນຳໃຊ້',
            content_type='video',
            content='<p>NumPy ສຳລັບການຄິດໄລ່ວິທະຍາສາດ...</p>',
            duration_minutes=25,
            order=1,
            is_preview=True
        )

        # Chapter 2
        chapter2 = CourseChapter.objects.create(
            course=course,
            title='Pandas DataFrames',
            description='ເຮັດວຽກກັບ Pandas',
            order=2
        )

        Lesson.objects.create(
            course=course,
            chapter=chapter2,
            title='ແນະນຳ Pandas',
            slug='intro-to-pandas',
            description='Pandas DataFrames ພື້ນຖານ',
            content_type='video',
            content='<p>Pandas ສຳລັບການວິເຄາະຂໍ້ມູນ...</p>',
            duration_minutes=28,
            order=1
        )

        course.update_total_lessons()
        course.update_duration()

    def _create_advanced_python_content(self, course):
        """Create chapters and lessons for Advanced Python course"""

        # Chapter 1
        chapter1 = CourseChapter.objects.create(
            course=course,
            title='Decorators ແລະ Generators',
            description='Advanced Python features',
            order=1
        )

        Lesson.objects.create(
            course=course,
            chapter=chapter1,
            title='Python Decorators',
            slug='python-decorators',
            description='ເຂົ້າໃຈແລະນຳໃຊ້ decorators',
            content_type='video',
            content='<p>Decorators ເປັນ feature ທີ່ມີພະລັງ...</p>',
            duration_minutes=35,
            order=1,
            is_preview=True
        )

        # Chapter 2
        chapter2 = CourseChapter.objects.create(
            course=course,
            title='Async Programming',
            description='Asynchronous Python',
            order=2
        )

        Lesson.objects.create(
            course=course,
            chapter=chapter2,
            title='Async/Await ພື້ນຖານ',
            slug='async-await-basics',
            description='ແນະນຳ asynchronous programming',
            content_type='video',
            content='<p>Async programming ໃນ Python...</p>',
            duration_minutes=40,
            order=1
        )

        course.update_total_lessons()
        course.update_duration()
