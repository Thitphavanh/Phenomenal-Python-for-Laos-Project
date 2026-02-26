from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse
from .models import Post

class LatestPostsFeed(Feed):
    title = "Python for Laos - Latest Posts"
    link = "/posts/"
    description = "Updates on changes and additions to pythonforlaos.com."

    def items(self):
        return Post.objects.filter(status='published').order_by('-published_at')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.content, 30)

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('blog:post_detail', args=[item.slug])
