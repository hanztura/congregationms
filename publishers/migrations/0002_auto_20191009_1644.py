# Generated by Django 2.2.6 on 2019-10-09 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publishers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publisher',
            name='contact_numbers',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='date_of_baptism',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
    ]
