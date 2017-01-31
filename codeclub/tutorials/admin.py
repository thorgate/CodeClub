from django.contrib import admin
from django.db import models

from markdownx.widgets import AdminMarkdownxWidget

from tutorials.models import Tutorial


class TutorialAdmin(admin.ModelAdmin):
    search_fields = ('title', 'author__email', 'author__name')
    list_filter = ('public',)
    list_display = ('title', 'public', 'author', 'order')
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }


admin.site.register(Tutorial, TutorialAdmin)
