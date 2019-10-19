import uuid

from enum import Enum

from django.db import models
from django.urls import reverse

from publishers.models import Publisher


# Create your models here.
class Pioneer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.SlugField(max_length=50, unique=True, blank=True)
    publisher = models.OneToOneField(Publisher, on_delete=models.CASCADE, related_name='pioneering')
    is_active = models.BooleanField(default=False, blank=True)


    class Meta:
        ordering = 'publisher__last_name', 'publisher__first_name', 'publisher__middle_name'

    def __str__(self):
        return str(self.publisher)

    def get_absolute_url(self):
        return reverse('pioneering:index')

    @property
    def slug(self):
        return self.code
    


class PioneerType(Enum):
    AU = 'Auxillary Pioneer'
    RP = 'Regular Pioneer'
    SP = 'Special Pioneer'


class PioneerDetail(models.Model):
    pioneer = models.ForeignKey(Pioneer, on_delete=models.CASCADE)
    pioneer_type = models.CharField(
        max_length=2, choices=[(p.name, p.value) for p in PioneerType]
    )
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)
