from django.views.generic import DetailView, ListView

from accounts.mixins import ProtectedMixin
from tutorials.models import Tutorial


class TutorialsListView(ProtectedMixin, ListView):
    model = Tutorial

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(public=True)

        return qs


class TutorialsDetailView(ProtectedMixin, DetailView):
    model = Tutorial

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(public=True)

        return qs
