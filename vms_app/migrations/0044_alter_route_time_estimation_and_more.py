# Generated by Django 5.0.1 on 2024-02-27 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vms_app", "0043_shift_km_estimation_shift_time_estimation_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="route",
            name="time_estimation",
            field=models.IntegerField(blank=True, default=100, null=True),
        ),
        migrations.AlterField(
            model_name="shift",
            name="time_estimation",
            field=models.FloatField(default=0, editable=False),
        ),
    ]
