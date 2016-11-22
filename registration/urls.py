from django.conf.urls import url
from . import views

app_name = 'registration'
urlpatterns = [
    # /registration/ i.e., home of app
    url(r'^$', views.index, name='index'),

    # /registration/<visitor_id>/ i.e., unique user page
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),

    # /registration/all/ i.e., see all users page
    url(r'^all', views.showallvisitors, name='showallvisitors'),

    # /registration/FilterAll/ i.e., see all users page
    url(r'^FilterAll', views.showallvisitorswithfilter, name='showallvisitorsWithFilter'),

    # /registration/register/ i.e., register a new visitor form
    url(r'^register', views.RegisterView.as_view(), name='register'),

    # /registration/showDetail/ i.e., show details of a visitor
    url(r'^showDetail', views.showdetail, name='showdetail'),

    # /registration/filter/ i.e., filter visitors by dates
    url(r'^filter', views.filtervisitors, name='filter'),

    # /registration/export/ i.e., export visitors data to excel
    url(r'^export', views.exporttoexcel, name='export'),

    ]