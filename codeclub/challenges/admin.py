from django.contrib import admin
from django.db import models

from markdownx.widgets import AdminMarkdownxWidget

from challenges.models import Event, Challenge, Solution


class EventAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_filter = ('public',)
    list_display = ('title', 'public')


class ChallengeAdmin(admin.ModelAdmin):
    search_fields = ['event__title']
    list_filter = ('event__public', 'public', 'golf', 'network_allowed', 'event', 'author')
    list_display = ('title', 'public', 'event', 'author', 'golf', 'network_allowed')
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }
    fieldsets = (
        (None, {'fields': ('event', 'title', 'public', 'author', 'order')}),
        ('Features', {'fields': ('points', 'golf', 'network_allowed')}),
        ('Testing', {'fields': ('tester', 'requirements', 'timeout')}),
        ('Description', {'fields': ('description',)}),
    )


class SolutionAdmin(admin.ModelAdmin):
    search_fields = ['user__email', 'user__name']
    list_filter = ('challenge__title', 'status')


admin.site.register(Event, EventAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Solution, SolutionAdmin)
