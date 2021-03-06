# Generated by Django 2.2.6 on 2019-10-09 16:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('last_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100)),
                ('date_of_birth', models.DateField(blank=True)),
                ('date_of_baptism', models.DateField(blank=True)),
                ('contact_numbers', models.CharField(max_length=200)),
            ],
        ),
    ]
