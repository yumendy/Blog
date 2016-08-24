from django.contrib.syndication.views import Feed
from django.urls import reverse, reverse_lazy
from article.models import Blog
from markdown import markdown


class LatestBlogFeed(Feed):
    title = 'yumendy\'s blog latest article.'
    link = reverse_lazy('homepage')
    description = 'yumendy\'s blog'

    def items(self):
        return Blog.objects.all()[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return markdown(item.summary)

    def item_link(self, item):
        return reverse('blog-detail', args=[item.pk])

    def item_author_name(self, item):
        return item.author.username

    def item_author_email(self, item):
        return item.author.email

    def item_pubdate(self, item):
        return item.publish_time

    def item_categories(self, item):
        return (item.category,)
