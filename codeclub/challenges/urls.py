from django.conf.urls import patterns, url

from challenges.views import (
    DashboardView, ChallengeListView, ChallengeDetailView, CodeOfConductView,
    ContestantsJSON, ChallengesJSON, ChallengeJSON, EventsJSON,
)


urlpatterns = patterns('accounts.views',
    url(r'^coc', CodeOfConductView.as_view(), name='coc'),
    url(r'^dashboard$', DashboardView.as_view(), name='dashboard'),
    url(r'^challenges$', ChallengeListView.as_view(), name='challenge_list'),
    url(r'^challenges/(?P<pk>[0-9]+)$', ChallengeDetailView.as_view(), name='challenge_detail'),

    url(r'^events_json$', EventsJSON.as_view(), name='events_json'),
    url(r'^contestants_json$', ContestantsJSON.as_view(), name='contestants_json'),
    url(r'^challenges_json$', ChallengesJSON.as_view(), name='challenges_json'),
    url(r'^challenge_json/(?P<pk>[0-9]+)$', ChallengeJSON.as_view(), name='challenge_json'),
)
