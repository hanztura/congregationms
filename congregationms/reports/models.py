from django.db import models
from django.urls import reverse

from pioneering.models import PioneerDetail
from publishers.models import Group, Publisher


# Create your models here.
class MonthlyFieldService(models.Model):
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.PROTECT, blank=True, null=True)
    pioneering = models.ForeignKey(PioneerDetail, on_delete=models.PROTECT, blank=True, null=True, related_name='mfs')
    month_ending = models.DateField()
    placements = models.PositiveSmallIntegerField(default=0)
    video_showing = models.PositiveSmallIntegerField(default=0)
    hours = models.PositiveSmallIntegerField(default=0)
    return_visits = models.PositiveSmallIntegerField(default=0)
    bible_study = models.PositiveSmallIntegerField(default=0)
    comments = models.CharField(max_length=255, blank=True)

    def __str__(self):
      name = str(self.publisher)
      return '{} for month ending {}'.format(name, self.month_ending)

    def get_absolute_url(self):
        return reverse('reports:mfs-detail', args=[str(self.pk)])
