from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login),
    url('board/', views.board),
    url('board', views.board),
    url('login/', views.login),
    url('login', views.login),
    url('get_ass', views.get_assignment),
    url('get_ass/', views.get_assignment),
    url('post_list', views.get_postlist),
    url('post_list/', views.get_postlist),
    url('post_add', views.post_add),
    url('post_add/', views.post_add),
    url('post_detail/(?P<pk>\d+)$', views.get_postdetail),
    url('post_detail/(?P<pk>\d+)/$', views.get_postdetail),
    url('post_detail/(?P<pk>\d+)/post/update$', views.post_update),
    url('post_detail/(?P<pk>\d+)/post/update/$', views.post_update),
    url('post_detail/(?P<pk>\d+)/post/delete$', views.post_delete),
    url('post_detail/(?P<pk>\d+)/post/delete/$', views.post_delete),
    url('post_detail/(?P<pk>\d+)/comment/add$', views.comment_add),
    url('post_detail/(?P<pk>\d+)/comment/add/$', views.comment_add),
    url('post_detail/(?P<pk>\d+)/comment/update/(?P<pk2>\d+)$', views.comment_update),
    url('post_detail/(?P<pk>\d+)/comment/update/(?P<pk2>\d+)/$', views.comment_update),
    url('post_detail/(?P<pk>\d+)/comment/delete/(?P<pk2>\d+)$', views.comment_delete),
    url('post_detail/(?P<pk>\d+)/comment/delete/(?P<pk2>\d+)/$', views.comment_delete)
]