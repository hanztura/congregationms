# Generated by Django 2.2.6 on 2019-12-06 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publishers', '0021_auto_20191205_1134'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='asset',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='group',
            name='color',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]