from django.contrib.syndication.views import Feed
from django.urls import reverse, reverse_lazy
from article.models import Blog
from markdown import markdown


class LatestBlogFeed(Feed):
    title = 'yumendy\'s blog latest article.'
    link = reverse_lazy('homepage')
    description = 'yumendy\'s blog latest article.'

    def items(self):
        return Blog.objects.all()[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return markdown(item.summary)

    def item_link(self, item):
        return reverse('blog-detail', args=[item.pk])



