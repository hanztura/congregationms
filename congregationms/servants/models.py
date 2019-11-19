from uuid import uuid4

from django.db import models
from django.urls import reverse_lazy

from simple_history.models import HistoricalRecords

from publishers.models import Publisher


class Servant(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    publisher = models.OneToOneField(
        Publisher, on_delete=models.PROTECT, related_name='servant')
    elder = models.BooleanField(default=False, blank=True)
    ms = models.BooleanField(default=False, blank=True,
                             verbose_name='Ministerial Servant')
    history = HistoricalRecords()

    class Meta:
        ordering = ('-elder', '-ms',
                    'publisher__last_name', 'publisher__first_name')

    def __str__(self):
        return self.publisher.name

    def get_absolute_url(self):
        return reverse_lazy('servants:detail', args=[str(self.pk)])

    @property
    def servant_type(self):
        _type = ''
        if self.elder:
            _type = 'Elder'
        elif self.ms:
            _type = 'Ministerial'

        return _type
