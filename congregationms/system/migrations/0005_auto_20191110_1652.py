# Generated by Django 2.2.6 on 2019-11-10 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_auto_20191106_0445'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='gmail_address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='gmail_password',
        ),
    ]