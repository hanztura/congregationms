# Generated by Django 2.2.6 on 2019-11-18 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publishers', '0012_usergroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='publisher',
            name='elderly',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='publisher',
            name='infirmed',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
