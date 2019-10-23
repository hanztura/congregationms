import uuid

from django.db import models
from django.urls import reverse

from system.models import Congregation as Cong


# Create your models here.
class Publisher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=False)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_baptism = models.DateField(blank=True, null=True)
    contact_numbers = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = 'last_name', 'first_name', 'middle_name'

    def __str__(self):
        name = self.name
        return name

    def get_absolute_url(self):
        return reverse('publishers:detail', args=[str(self.slug)])

    @property
    def name(self):
        name = '{}, {}'.format(self.last_name, self.first_name)
        return name

    @property
    def group(self):
        group = self.group_members.filter(is_active=True).first()

        if group:
            group = group.group
        return group

    @property
    def is_pioneer(self):
        try:
            pioneering = self.pioneering
        except Exception as e:
            pioneering = False
        finally:
            if pioneering:
                return pioneering.is_active

            return False

    def is_rp(self, date):
        try:
            pioneering = self.pioneering
        except Exception as e:
            pioneering = False
        finally:
            if pioneering:
                return pioneering.is_active_rp(date)

            return False


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    congregation = models.ForeignKey(Cong, on_delete=models.CASCADE)

    def __str__(self):
        return '{} at {}'.format(self.name, self.congregation)

    def get_absolute_url(self):
        return reverse('publishers:group-detail', args=[str(self.pk)])

    @property
    def members(self):
        members = self.group_members.all()
        members = [member.publisher for member in members]

        return members


class Member(models.Model):
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='group_members')
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, related_name='group_members')
    is_active = models.BooleanField(default=False)
    date_from = models.DateField(blank=True, null=True, verbose_name='from')
    date_to = models.DateField(blank=True, null=True, verbose_name='to')

    def __str__(self):
        return '{} in Group {}'.format(self.publisher, self.group)

    @property
    def group_name(self):
        return str(self.group)
