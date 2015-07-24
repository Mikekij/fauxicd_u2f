from django.conf.urls import patterns, url
from web import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^icd_index/', views.icd_index, name='icd_index'),

        )
