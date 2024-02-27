# Generated by Django 5.0.1 on 2024-02-26 15:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vms_app", "0041_rename_end_shift_end_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="triphistory",
            name="shift",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="shift_trips_set",
                to="vms_app.shift",
            ),
        ),
        migrations.AlterField(
            model_name="triphistory",
            name="trip_count",
            field=models.IntegerField(default=0),
        ),
    ]