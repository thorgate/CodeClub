from django.conf.urls import patterns, url

from tutorials import views


urlpatterns = patterns('accounts.views',
    url(r'^tutorials$', views.TutorialsListView.as_view(), name='tutorials_list'),
    url(r'^tutorials/(?P<pk>[0-9]+)$', views.TutorialsDetailView.as_view(), name='tutorials_detail'),
)
