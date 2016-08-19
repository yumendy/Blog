from django.conf.urls import url
from website import views
from website.feeds import LatestBlogFeed


urlpatterns = [
    url(r'^$', views.HomepageView.as_view(), name='homepage'),
    url(r'^dashboard/$', views.DashboardOverviewView.as_view(), name='dashboard'),
    url(r'^about/$', views.AboutMeView.as_view(), name='about'),
    url(r'^guest/$', views.GuestBookView.as_view(), name='guest'),
    url(r'^feed/$', LatestBlogFeed()),
]
