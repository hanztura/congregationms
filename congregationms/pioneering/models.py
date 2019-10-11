import uuid

from enum import Enum

from django.db import models

from publishers.models import Publisher


# Create your models here.
class Pioneer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, unique=True, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.publisher)


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
