# Generated by Django 2.2.6 on 2019-11-25 00:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publishers', '0017_auto_20191119_1837'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalpublisher',
            name='elder',
        ),
        migrations.RemoveField(
            model_name='historicalpublisher',
            name='ministerial_servant',
        ),
        migrations.RemoveField(
            model_name='publisher',
            name='elder',
        ),
        migrations.RemoveField(
            model_name='publisher',
            name='ministerial_servant',
        ),
    ]
