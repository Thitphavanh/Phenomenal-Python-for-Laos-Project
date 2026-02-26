from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from blog.models import Post, Category, Tag
import random
import json
import os

class Command(BaseCommand):
    help = 'ສ້າງບົດຄວາມເທັກໂນໂລຊີ - ສາມາດເພີ່ມບົດຄວາມໃໝ່ໄດ້ງ່າຍ'

    def add_arguments(self, parser):
        parser.add_argument(
            '--add-post',
            action='store_true',
            help='ເພີ່ມບົດຄວາມໃໝ່ຈາກໄຟລ໌ JSON',
        )
        parser.add_argument(
            '--post-file',
            type=str,
            help='ທີ່ຢູ່ໄຟລ໌ JSON ທີ່ມີຂໍ້ມູນບົດຄວາມ',
            default='new_posts.json'
        )

    def handle(self, *args, **options):
        if options['add_post']:
            self.add_posts_from_file(options['post_file'])
            return
            
        # ສ້າງ Categories
        self.create_categories()
        
        # ສ້າງ Tags
        self.create_tags()
        
        # ໃຊ້ user admin ຫຼື ສ້າງໃໝ່
        author = self.get_author()
        if not author:
            return
            
        # ສ້າງບົດຄວາມທັງໝົດ
        self.create_all_posts(author)
        
        self.stdout.write(
            self.style.SUCCESS('ສ້າງບົດຄວາມສໍາເລັດແລ້ວ!')
        )

    def create_categories(self):
        """ສ້າງໝວດໝູ່ຕ່າງໆ"""
        categories_data = [
            {
                'name': 'ປັນຍາປະດິດ (AI)',
                'slug': 'artificial-intelligence',
                'description': 'ບົດຄວາມກ່ຽວກັບເທັກໂນໂລຊີປັນຍາປະດິດ'
            },
            {
                'name': 'ລົດໄຟຟ້າ (EV)',
                'slug': 'electric-vehicles',
                'description': 'ຂ່າວສານ ແລະ ຂໍ້ມູນກ່ຽວກັບລົດໄຟຟ້າ'
            },
            {
                'name': 'ແບັດເຕີຣີ',
                'slug': 'battery-technology',
                'description': 'ເທັກໂນໂລຊີແບັດເຕີຣີ ແລະ ການເກັບຮັກສາພະລັງງານ'
            },
            {
                'name': 'ຊອບແວ',
                'slug': 'software',
                'description': 'ການພັດທະນາຊອບແວ ແລະ ແອັບພລິເຄຊັນ'
            },
            {
                'name': 'ຮາດແວ',
                'slug': 'hardware',
                'description': 'ອຸປະກອນຄອມພິວເຕີ ແລະ ເທັກໂນໂລຊີຮາດແວ'
            },
            {
                'name': 'ເທັກໂນໂລຊີໃນລາວ',
                'slug': 'tech-in-laos',
                'description': 'ການພັດທະນາເທັກໂນໂລຊີໃນ ສປປ ລາວ'
            },
            {
                'name': 'ພະລັງງານທົດແທນ',
                'slug': 'renewable-energy',
                'description': 'ພະລັງງານແສງຕາເວັນ, ລົມ, ແລະ ທົດແທນອື່ນໆ'
            }
        ]

        self.categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description']
                }
            )
            self.categories[cat_data['slug']] = category
            if created:
                self.stdout.write(f"ສ້າງໝວດໝູ່: {category.name}")

    def create_tags(self):
        """ສ້າງແທັກຕ່າງໆ"""
        tags_data = [
            'AI', 'Machine Learning', 'Deep Learning', 'Neural Network', 'ChatGPT',
            'Tesla', 'Electric Car', 'Sustainable Transport', 'Charging', 'EV',
            'Lithium Battery', 'Solar Battery', 'Energy Storage', 'Solar Power',
            'Python', 'JavaScript', 'Mobile App', 'Web Development', 'Programming',
            'Processor', 'GPU', 'RAM', 'SSD', 'Innovation', 'Future Tech',
            'Laos Development', 'Green Energy', 'Smart City', 'IoT', 'Blockchain',
            '5G', 'Cloud Computing', 'Cybersecurity', 'Big Data', 'Robotics'
        ]

        self.tags = {}
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(
                slug=slugify(tag_name),
                defaults={'name': tag_name}
            )
            self.tags[tag_name] = tag
            if created:
                self.stdout.write(f"ສ້າງແທັກ: {tag.name}")

    def get_author(self):
        """ຊອກຫາ ຫຼື ສ້າງ author"""
        try:
            author = User.objects.get(username='admin')
        except User.DoesNotExist:
            author = User.objects.filter(is_superuser=True).first()
            if not author:
                self.stdout.write(
                    self.style.ERROR('ກະລຸນາສ້າງ superuser ກ່ອນ: python manage.py createsuperuser')
                )
                return None
        return author

    def create_all_posts(self, author):
        """ສ້າງບົດຄວາມທັງໝົດ"""
        posts_data = self.get_posts_data()
        
        for post_data in posts_data:
            self.create_single_post(post_data, author)

    def create_single_post(self, post_data, author):
        """ສ້າງບົດຄວາມດຽວ"""
        # ສ້າງ Post
        post, created = Post.objects.get_or_create(
            slug=slugify(post_data['title']),
            defaults={
                'title': post_data['title'],
                'content': post_data['content'],
                'excerpt': post_data['excerpt'],
                'author': author,
                'category': self.categories[post_data['category']],
                'status': 'published',
                # 'featured': random.choice([True, False]),
                # 'published_date': timezone.now()
            }
        )

        if created:
            # ເພີ່ມ Tags
            post_tags = [self.tags[tag_name] for tag_name in post_data['tags'] 
                        if tag_name in self.tags]
            post.tags.set(post_tags)
            
            self.stdout.write(f"ສ້າງບົດຄວາມ: {post.title}")
        else:
            self.stdout.write(f"ມີແລ້ວ: {post.title}")

    def add_posts_from_file(self, file_path):
        """ເພີ່ມບົດຄວາມຈາກໄຟລ໌ JSON"""
        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.ERROR(f'ບໍ່ພົບໄຟລ໌: {file_path}')
            )
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                new_posts = json.load(f)
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(f'ໄຟລ໌ JSON ບໍ່ຖືກຕ້ອງ: {file_path}')
            )
            return

        # ໃຫ້ແນ່ໃຈວ່າມີ categories ແລະ tags
        self.create_categories()
        self.create_tags()
        
        author = self.get_author()
        if not author:
            return

        for post_data in new_posts:
            self.create_single_post(post_data, author)

        self.stdout.write(
            self.style.SUCCESS(f'ເພີ່ມບົດຄວາມຈາກ {file_path} ສໍາເລັດແລ້ວ!')
        )

    def get_posts_data(self):
        """ຂໍ້ມູນບົດຄວາມທັງໝົດ"""
        return [
            {
                'title': 'ປັນຍາປະດິດ (AI) ກໍາລັງປ່ຽນແປງໂລກແນວໃດ?',
                'category': 'artificial-intelligence',
                'tags': ['AI', 'Machine Learning', 'Innovation', 'Future Tech'],
                'excerpt': 'ຄົ້ນພົບວ່າເທັກໂນໂລຊີ AI ກໍາລັງສ້າງການປ່ຽນແປງອັນໃຫຍ່ຫຼວງໃນທຸກຂະແໜງການ ແຕ່ການແພດຈົນເຖິງການສຶກສາ',
                'content': '''ປັນຍາປະດິດ (Artificial Intelligence) ຫຼື AI ແມ່ນເທັກໂນໂລຊີທີ່ກໍາລັງປ່ຽນແປງໂລກຂອງພວກເຮົາຢ່າງຮວດເຮັວ...'''
            },
            {
                'title': '5G Technology: ການປະວັດການເຊື່ອມຕໍ່ແບບໃໝ່',
                'category': 'hardware',
                'tags': ['5G', 'Innovation', 'Future Tech', 'Mobile'],
                'excerpt': '5G ຈະປ່ຽນແປງວິທີທີ່ພວກເຮົາໃຊ້ອິນເຕີເນັດ ແລະ ເຊື່ອມຕໍ່ອຸປະກອນຕ່າງໆ',
                'content': '''5G ແມ່ນເຄືອຂ່າຍໄຮ້ສາຍລຸ້ນທີ 5 ທີ່ສັນຍາວ່າຈະໃຫ້ຄວາມໄວທີ່ໄວກວ່າ 4G ເຖິງ 100 ເທົ່າ...'''
            },
            {
                'title': 'Blockchain ແລະ Cryptocurrency ໃນລາວ',
                'category': 'tech-in-laos',
                'tags': ['Blockchain', 'Cryptocurrency', 'Laos Development', 'Innovation'],
                'excerpt': 'ຄວາມເປັນໄປໄດ້ຂອງການນໍາໃຊ້ Blockchain ແລະ Cryptocurrency ໃນການພັດທະນາເສດຖະກິດດິຈິຕອນຂອງລາວ',
                'content': '''Blockchain ແມ່ນເທັກໂນໂລຊີທີ່ຢູ່ເບື້ອງຫຼັງ Bitcoin ແລະ Cryptocurrency ອື່ນໆ...'''
            }
            # ສາມາດເພີ່ມບົດຄວາມອື່ນໆໄດ້ຕາມການຕ້ອງການ
        ]
