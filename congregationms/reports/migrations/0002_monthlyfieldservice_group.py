# Generated by Django 2.2.6 on 2019-10-16 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publishers', '0007_auto_20191015_2021'),
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlyfieldservice',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='publishers.Group'),
        ),
    ]
