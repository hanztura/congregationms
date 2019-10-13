from django.db import models
from django.urls import reverse

from publishers.models import Publisher


# Create your models here.
class MonthlyFieldService(models.Model):
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
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
