# Generated by Django 5.0.1 on 2024-02-26 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vms_app', '0034_alter_route_time_estimation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='time_estimation',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shift',
            name='time_estimation',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
