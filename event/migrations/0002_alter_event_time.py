# Generated by Django 4.2.13 on 2024-05-29 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]