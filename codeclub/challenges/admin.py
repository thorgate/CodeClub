from django.contrib import admin

from challenges.models import Event, Challenge, Solution


class SolutionAdmin(admin.ModelAdmin):
    search_fields = ['user__email', 'user__name']
    list_filter = ('challenge__title', 'status')

admin.site.register(Event)
admin.site.register(Challenge)
admin.site.register(Solution, SolutionAdmin)
