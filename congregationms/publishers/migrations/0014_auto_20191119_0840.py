# Generated by Django 2.2.6 on 2019-11-19 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('publishers', '0013_auto_20191118_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='publisher',
            name='elder',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='publisher',
            name='ministerial_servant',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.CreateModel(
            name='HistoricalPublisher',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('slug', models.SlugField()),
                ('last_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('date_of_baptism', models.DateField(blank=True, null=True)),
                ('contact_numbers', models.CharField(blank=True, max_length=200)),
                ('infirmed', models.BooleanField(blank=True, default=False)),
                ('elderly', models.BooleanField(blank=True, default=False)),
                ('elder', models.BooleanField(blank=True, default=False)),
                ('ministerial_servant', models.BooleanField(blank=True, default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical publisher',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]