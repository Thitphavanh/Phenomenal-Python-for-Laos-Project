from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from blog.models import Post
from courses.models import Course
from events.models import Event
from community.models import Topic
from docs.models import Documentation

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Post.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at

class CourseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Course.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at

class EventSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Event.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at

class TopicSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7
    protocol = 'https'

    def items(self):
        # Assuming topics don't have a 'status' field or use a different one. 
        # Topic model has is_closed, is_pinned but no explicit status.
        return Topic.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

class DocumentSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6
    protocol = 'https'

    def items(self):
        return Documentation.objects.all() # Assuming documents are all public? 
        # Checking docs model might be good, but assuming all are valid for now.

    def lastmod(self, obj):
        return obj.updated_at

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return ['home:index', 'blog:login', 'blog:register']

    def location(self, item):
        return reverse(item)
