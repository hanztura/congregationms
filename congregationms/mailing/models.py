from uuid import uuid4

from django.db import models

from system.models import User


class UserMail(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='mail')
    server = models.CharField(max_length=200)
    tls = models.BooleanField(default=True)
    tls_port = models.SmallIntegerField(default=587)
    name = models.CharField(max_length=200)
    email_address = models.CharField(max_length=200)
    password = models.CharField(max_length=64)

    def __str__(self):
        return self.email_address


class Mail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user_mail = models.ForeignKey(UserMail, on_delete=models.PROTECT, blank=True)
    to = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return '{} "{}"'.format(str(self.user_mail), self.subject)
