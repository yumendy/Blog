from django.conf.urls import url
from authentication import views

urlpatterns = [
    url(r'^user/logout/$', views.LogoutView.as_view(), name='user-logout'),
    url(r'^user/login/$', views.LoginView.as_view(), name='user-login'),
]
