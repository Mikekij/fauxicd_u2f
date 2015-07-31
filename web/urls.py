from django.conf.urls import patterns, url
from web import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^icd_index/', views.icd_index, name='icd_index'),
        url(r'^add_icd/$', views.add_icd, name="add_icd"),
        url(r'^edit_icd/(?P<id>\d+)/$', views.edit_icd, name='edit_icd'),
        url(r'^deliver_shock/$', views.deliver_shock, name="deliver_shock"),
        )