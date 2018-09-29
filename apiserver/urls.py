from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list),
    url('board/', views.board),
    url('board', views.board),
    url('login/', views.login),
    url('login', views.login),
    url('get_ass', views.get_assignment),
    url('get_ass/', views.get_assignment),
    url('post_list', views.get_postlist),
    url('post_list/', views.get_postlist),
    url('post_detail/(?P<pk>\d+)$', views.get_postdetail),
    url('post_detail/(?P<pk>\d+)/$', views.get_postdetail)
]