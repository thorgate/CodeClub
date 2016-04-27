import json
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import dateformat, timezone
from django.views.generic import View, TemplateView, DetailView
from django.views.generic.detail import BaseDetailView

from accounts.mixins import ProtectedMixin
from accounts.models import User
from challenges.forms import SolutionForm
from challenges.models import Challenge, Solution, Event


class DashboardView(TemplateView):
    template_name = "challenges/dashboard.html"


class ChallengeListView(ProtectedMixin, TemplateView):
    template_name = 'challenges/challenge_list.html'


class ChallengeDetailView(ProtectedMixin, DetailView):
    model = Challenge
    context_object_name = 'challenge'

    def get(self, request, *args, **kwargs):
        self.queryset = Challenge.objects.filter(event__public=True, public=True)
        if request.user.is_staff:
            self.queryset = Challenge.objects.all()

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        form = SolutionForm(request.POST or None, files=request.FILES or None, user=self.request.user, challenge=self.object)

        if form.is_valid():
            form.save()
            return redirect(self.object)

        context['form'] = form

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self.get(request, args, **kwargs)


class EventsJSON(View):

    def get(self, request, *args, **kwargs):
        events = Event.objects.filter(public=True)
        if request.user.is_staff:
            events = Event.objects.all()

        events = events.order_by("-start_time")
        return JSONResponse([event.serialize() for event in events])


class ContestantsJSON(View):

    def get(self, request, *args, **kwargs):
        solutions = Solution.objects.filter(
            challenge__event__public=True, challenge__public=True, status=Solution.STATUS_CORRECT,
        )

        try:
            event = Event.objects.get(id=int(request.GET['event']))
        except (KeyError, ValueError, Event.DoesNotExist):
            pass
        else:
            solutions = solutions.filter(challenge__event=event)

        solutions = solutions.order_by('user_id', '-challenge_id')
        solutions = solutions.distinct('user_id', 'challenge_id')
        solutions = solutions.select_related('user', 'challenge')
        contestants = {}

        for solution in solutions:
            user = solution.user
            if user.id not in contestants:
                contestants[user.id] = {
                    'id': user.id,
                    'name': user.get_display_name(),
                    'challenges': 0,
                    'score': 0,
                }

            contestant = contestants[user.id]
            contestant['challenges'] += 1
            contestant['score'] += solution.challenge.calculated_points

        contestants = sorted(contestants.values(), key=lambda c: (-c['score'], -c['challenges'], c['name'].lower()))

        return JSONResponse(contestants)


class ChallengesJSON(ProtectedMixin, View):

    def get(self, request, *args, **kwargs):
        qs = Challenge.objects.filter(event__public=True, public=True)
        if request.user.is_staff:
            qs = Challenge.objects.all()
        qs = qs.select_related('event')

        challenges = sorted(qs, key=lambda c: c.calculated_points)

        solved_ids = Solution.objects.filter(
            user=self.request.user, status=Solution.STATUS_CORRECT
        ).distinct('challenge_id').values_list('challenge_id', flat=True)

        events = {}
        for challenge in challenges:
            if challenge.event_id not in events:
                event = challenge.event
                events[event.id] = event.serialize()
                events[event.id]['challenges'] = []
            events[challenge.event_id]['challenges'].append(challenge.serialize())

        return JSONResponse({
            'solved_ids': list(solved_ids),
            'events': sorted(events.values(), key=lambda e: e['start_time'], reverse=True),
        })


class ChallengeJSON(ProtectedMixin, BaseDetailView):

    model = Challenge

    def get(self, request, *args, **kwargs):
        self.queryset = Challenge.objects.filter(event__public=True, public=True)
        if request.user.is_staff:
            self.queryset = Challenge.objects.all()

        self.object = self.get_object()

        solutions = self.object.solution_set.filter(user=self.request.user).order_by('-timestamp')

        order_columns = ['timestamp']
        if self.object.golf:
            order_columns.insert(0, 'solution_size')

        # We could use DISTINCT ON user_id, but it only works in PostgreSQL
        all_correct_solutions = self.object.solution_set.filter(
            status=Solution.STATUS_CORRECT,
        ).order_by(*order_columns).select_related('user')

        # Do the mapping in memory so that we have the correct order of the users
        # Cache is used for detecting if we have already added the user to the list or not
        correct_user_cache = []
        correct_users = []
        for solution in all_correct_solutions:
            if solution.user_id not in correct_user_cache:
                correct_user_cache.append(solution.user_id)
                correct_users.append((solution.user.get_display_name(), solution.solution_size))

        return JSONResponse({
            'challenge': self.object.serialize(),
            'solutions': [s.serialize() for s in solutions],
            'correct_users': correct_users,
        })


class CodeClubEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return dateformat.format(obj.astimezone(timezone.get_default_timezone()), 'd. F - H:i')


class JSONResponse(HttpResponse):
    def __init__(self, content, cls=CodeClubEncoder):
        super(JSONResponse, self).__init__(json.dumps(content, cls=cls), content_type='application/json')
