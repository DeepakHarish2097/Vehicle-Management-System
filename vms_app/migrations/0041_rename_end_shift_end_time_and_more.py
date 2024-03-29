# Generated by Django 5.0.1 on 2024-02-26 14:59

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vms_app", "0040_alter_shift_routes"),
    ]

    operations = [
        migrations.RenameField(
            model_name="shift",
            old_name="end",
            new_name="end_time",
        ),
        migrations.RenameField(
            model_name="shift",
            old_name="created_date",
            new_name="shift_date",
        ),
        migrations.RenameField(
            model_name="vehicle",
            old_name="type",
            new_name="vehicle_type",
        ),
        migrations.AlterUniqueTogether(
            name="shift",
            unique_together={("shift_name", "vehicle", "shift_date")},
        ),
        migrations.AddField(
            model_name="shift",
            name="shift_remark",
            field=models.TextField(default="usual"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="shift",
            name="start_time",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name="shift",
            name="day_production",
        ),
        migrations.RemoveField(
            model_name="shift",
            name="fifth_trip_ton",
        ),
        migrations.RemoveField(
            model_name="shift",
            name="first_trip_ton",
        ),
        migrations.RemoveField(
            model_name="shift",
            name="fourth_trip_ton",
        ),
        migrations.RemoveField(
            model_name="shift",
            name="km_estimation",
        ),
        migrations.RemoveField(
            model_name="shift",
            name="second_trip_ton",
        ),
        migrations.RemoveField(
            model_name="shift",
            name="sixth_trip_ton",
        ),
        migrations.RemoveField(
            model_name="shift",
            name="start",
        ),
        migrations.RemoveField(
            model_name="shift",
            name="third_trip_ton",
        ),
        migrations.RemoveField(
            model_name="shift",
            name="time_estimation",
        ),
        migrations.RemoveField(
            model_name="shift",
            name="total_trip",
        ),
        migrations.RemoveField(
            model_name="shift",
            name="trip_ton",
        ),
    ]
