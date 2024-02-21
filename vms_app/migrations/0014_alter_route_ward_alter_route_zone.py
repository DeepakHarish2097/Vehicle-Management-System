# Generated by Django 5.0.1 on 2024-02-21 06:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vms_app', '0013_alter_ward_is_active_alter_zone_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='ward',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='ward_routes_set', to='vms_app.ward'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='route',
            name='zone',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='zone_routes_set', to='vms_app.zone'),
            preserve_default=False,
        ),
    ]
