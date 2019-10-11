import uuid

from django.db import models
from django.urls import reverse

from system.models import Congregation as Cong


# Create your models here.
class Publisher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_baptism = models.DateField(blank=True, null=True)
    contact_numbers = models.CharField(max_length=200, blank=True)

    def __str__(self):
        name = self.name
        return name

    def get_absolute_url(self):
        return reverse('publishers:detail', args=[str(self.pk)])

    @property
    def name(self):
        name = '{}, {}'.format(self.last_name, self.first_name)
        return name


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    congregation = models.ForeignKey(Cong, on_delete=models.CASCADE)

    def __str__(self):
        return '{} at {}'.format(self.name, self.congregation)


class Member(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    date_from = models.DateField(blank=True, null=True, verbose_name='from')
    date_to = models.DateField(blank=True, null=True, verbose_name='to')

    def __str__(self):
        return '{} in Group {}'.format(self.publisher, self.group)
