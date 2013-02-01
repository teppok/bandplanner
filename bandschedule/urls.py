from django.conf.urls import patterns, include, url

from bandschedule import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bandplanner.views.home', name='home'),
    # url(r'^bandplanner/', include('bandplanner.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', views.new_calendar_request, name='new_calendar'),
    url(r'^submit$', views.create_calendar_request, name='create_calendar'),
    url(r'^toggle$', views.toggle_date_request, name='toggle_date'),
    url(r'^month_seen$', views.approve_month_request, name='approve_month_request'),
    url(r'^get_month$', views.get_month_request, name='get_month'),
    url(r'^login_user$', views.login_user_request, name='login_user'),
    url(r'^logout_user$', views.logout_user_request, name='logout_user'),
    url(r'^(?P<calendar_id>\d+)/$', views.monthly_view_request, name='monthly_view'),
    url(r'^(?P<calendar_id>\d+)/(?P<year>\d+)/$', views.monthly_view_request, name='monthly_view2'),
    url(r'^(?P<calendar_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/$', views.monthly_view_request, name='monthly_view3'),
)
