from django.contrib import admin

from tutorials import models


class TutorialAdmin(admin.ModelAdmin):
    search_fields = ('title', 'author__email', 'author__name')
    list_filter = ('public',)
    list_display = ('title', 'public', 'author', 'order')


admin.site.register(models.Tutorial, TutorialAdmin)
