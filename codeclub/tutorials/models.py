from django.core.urlresolvers import reverse
from django.db import models


class Tutorial(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()
    public = models.BooleanField(default=True)
    author = models.ForeignKey("accounts.User", blank=True, null=True, on_delete=models.SET_NULL)

    order = models.IntegerField(help_text="In ascending order")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tutorials_detail', kwargs={'pk': self.pk})
