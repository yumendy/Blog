from article.mixin import CategoryMixin
from link.mixin import LinkListMixin
from mood.mixin import LeastMoodMixin
from navbar.mixin import NavBarMixin


class FrontMixin(NavBarMixin, LeastMoodMixin, CategoryMixin, LinkListMixin):
    def get_context_data(self, *args, **kwargs):
        return super(FrontMixin, self).get_context_data(*args, **kwargs)
