# Generated by Django 5.0.1 on 2024-03-17 11:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vms_app", "0052_maintanence_alter_fuelmaster_vehicle_jobcard"),
    ]

    operations = [
        migrations.CreateModel(
            name="MaintenanceSchedules",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("odo_closing", models.FloatField(default=0)),
                (
                    "service",
                    models.CharField(
                        choices=[
                            (
                                "SS1 WITH ENGINE OIL & FILTER",
                                "SS1 WITH ENGINE OIL & FILTER",
                            ),
                            (
                                "SS Gen WITHOUT ENGINE OIL & FILTER",
                                "SS Gen WITHOUT ENGINE OIL & FILTER",
                            ),
                            ("SS2", "SS2"),
                            ("SS3", "SS3"),
                            ("SS4", "SS4"),
                        ],
                        max_length=250,
                    ),
                ),
                ("scheduled_date", models.DateField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("Done", "Done"), ("Pending", "Pending")],
                        max_length=50,
                    ),
                ),
                (
                    "vehicle",
                    models.ForeignKey(
                        limit_choices_to={"is_active": True},
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="vehicle_shcedule_history",
                        to="vms_app.vehicle",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Maintanence",
        ),
    ]