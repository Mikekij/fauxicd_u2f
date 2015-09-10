from django.conf.urls import patterns, url
from web import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^register/$',views.register,name='register'),
        url(r'^login/$',views.user_login,name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^tfa_stub/$', views.tfa_stub, name='tfa_stub'),
        url(r'^user/(?P<id>\d+)/$', views.show_user, name='show_user'),
        url(r'^users/', views.users, name='users'),
        url(r'^edit_user/(?P<id>\d+)/$', views.edit_user, name='edit_user'),
        url(r'^icd_index/', views.icd_index, name='icd_index'),
        url(r'^icd/(?P<id>\d+)/$', views.show_icd, name='show_icd'),
        url(r'^add_icd/$', views.add_icd, name="add_icd"),
        url(r'^edit_icd/(?P<id>\d+)/$', views.edit_icd, name='edit_icd'),
        url(r'^deliver_shock_page/$', views.deliver_shock_page, name="deliver_shock_page"),
        url(r'^deliver_shock_ajax/$', views.deliver_shock_ajax, name="deliver_shock_ajax"),
        )
