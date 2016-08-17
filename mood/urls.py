from django.conf.urls import url
from mood import views

urlpatterns = [
    url(r'^add/$', views.MoodCreateView.as_view(), name='mood-add'),
    url(r'^list/$', views.MoodListView.as_view(), name='mood-list'),
    url(r'^(?P<pk>[0-9]+)/update/$', views.MoodUpdateView.as_view(), name='mood-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.MoodDeleteView.as_view(), name='mood-delete'),
    url(r'^timeline/$', views.MoodTimeLineView.as_view(), name='mood-time-line')
]
