import uuid
from datetime import datetime

from enum import Enum

from django.db import models
from django.urls import reverse

from publishers.models import Publisher
from publishers.utils import OrderByPublisherMixin


# Create your models here.
class Pioneer(OrderByPublisherMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.SlugField(max_length=50, unique=True, blank=True)
    publisher = models.OneToOneField(
        Publisher, on_delete=models.CASCADE, related_name='pioneering')
    is_active = models.BooleanField(default=False, blank=True, editable=False)

    def __str__(self):
        return str(self.publisher)

    def get_absolute_url(self):
        return reverse('pioneering:index')

    @property
    def name(self):
        return str(self.publisher)

    @property
    def slug(self):
        return self.code

    def save(self, *args, **kwargs):
        active = False
        pioneer_details = self.details.filter(has_ended=False)
        if pioneer_details.count() > 0:
            active = True
        self.is_active = active
        super().save(*args, **kwargs)

    def is_active_rp(self, date=None):
        """
        Check if a pioneer is RP on a given date
        """
        DATE_NOW = datetime.now().date()
        if not date:
            date = DATE_NOW
        active = False
        pioneer_details = self.details.filter(
            pioneer_type='RP',
            date_start__lte=date
        )
        pioneer_details_not_ended = pioneer_details.filter(
            date_end__gte=date).first()
        pioneer_details_continous = pioneer_details.filter(
            date_end=None).first()
        if pioneer_details_not_ended or pioneer_details_continous:
            active = True

        return active

    def get_active_pioneer_detail(self, date=None):
        DATE_NOW = datetime.now().date()
        if not date:
            date = DATE_NOW
        pioneer_details = self.details.filter(
            date_start__lte=date
        )
        pioneer_details_not_ended = pioneer_details.filter(
            date_end__gte=date).first()
        if pioneer_details_not_ended:
            return pioneer_details_not_ended

        pioneer_details_continous = pioneer_details.filter(
            date_end=None).first()
        if pioneer_details_continous:
            return pioneer_details_continous

        return None

    def get_active_rp_detail(self, date=None):
        DATE_NOW = datetime.now().date()
        if not date:
            date = DATE_NOW
        pioneer_details = self.details.filter(
            pioneer_type='RP',
            date_start__lte=date
        )
        pioneer_details_not_ended = pioneer_details.filter(
            date_end__gte=date).first()
        if pioneer_details_not_ended:
            return pioneer_details_not_ended

        pioneer_details_continous = pioneer_details.filter(
            date_end=None).first()
        if pioneer_details_continous:
            return pioneer_details_continous

        return None


class PioneerType(Enum):
    AU = 'Auxillary Pioneer'
    RP = 'Regular Pioneer'
    SP = 'Special Pioneer'


class PioneerDetail(models.Model):
    pioneer = models.ForeignKey(
        Pioneer, on_delete=models.CASCADE, related_name='details')
    pioneer_type = models.CharField(
        max_length=2, choices=[(p.name, p.value) for p in PioneerType]
    )
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)
    has_ended = models.BooleanField(default=False, blank=True, editable=False)

    def __str__(self):
        name = '{} - {}'.format(self.pioneer.name, self.pioneer_type)
        return name

    def save(self, *args, **kwargs):
        if not self.has_ended:
            DATE_NOW = datetime.now().date()
            date_end = self.date_end
            date_now = DATE_NOW
            if date_end:
                if date_now > date_end:
                    self.has_ended = True

        super().save(*args, **kwargs)

    @property
    def publisher(self):
        return self.pioneer.publisher
