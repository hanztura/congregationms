# Generated by Django 2.2.6 on 2019-11-19 17:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('publishers', '0014_auto_20191119_0840'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='publisher',
            name='assets',
            field=models.ManyToManyField(blank=True, null=True, related_name='publishers', to='publishers.Asset'),
        ),
    ]
