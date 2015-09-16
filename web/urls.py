from django.conf.urls import patterns, url
from web import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^register/$',views.register,name='register'),
        url(r'^login/$',views.user_login,name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^new_tfa_registration/$', views.new_tfa_registration, name='new_tfa_registration'),
        url(r'^create_tfa_registration/$', views.create_tfa_registration, name='create_tfa_registration'),
        url(r'^new_tfa_authentication/$', views.new_tfa_authentication, name='new_tfa_authentication'),
        url(r'^create_tfa_authentication/$', views.create_tfa_authentication, name='create_tfa_authentication'),
        url(r'^user/(?P<id>\d+)/$', views.show_user, name='show_user'),
        url(r'^users/', views.users, name='users'),
        url(r'^edit_user/(?P<id>\d+)/$', views.edit_user, name='edit_user'),
        url(r'^icd_index/', views.icd_index, name='icd_index'),
        url(r'^icd/(?P<id>\d+)/$', views.show_icd, name='show_icd'),
        url(r'^add_icd/$', views.add_icd, name="add_icd"),
        url(r'^edit_icd/(?P<id>\d+)/$', views.edit_icd, name='edit_icd'),
        url(r'^deliver_shock_page/$', views.deliver_shock_page, name="deliver_shock_page"),
        url(r'^deliver_shock_ajax/$', views.deliver_shock_ajax, name="deliver_shock_ajax"),
        url(r'^test_api_call/$', views.test_api_call, name="test_api_call")
        )
