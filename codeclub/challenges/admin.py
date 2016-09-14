from django.contrib import admin

from challenges.models import Event, Challenge, Solution


class EventAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_filter = ('public',)
    list_display = ('title', 'public')


class ChallengeAdmin(admin.ModelAdmin):
    search_fields = ['event__title']
    list_filter = ('event', 'event__public', 'public', 'author', 'golf')
    list_display = ('title', 'public', 'event', 'author', 'golf')


class SolutionAdmin(admin.ModelAdmin):
    search_fields = ['user__email', 'user__name']
    list_filter = ('challenge__title', 'status')


admin.site.register(Event, EventAdmin)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Solution, SolutionAdmin)
