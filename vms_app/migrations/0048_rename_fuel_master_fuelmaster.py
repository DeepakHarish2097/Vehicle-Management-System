# Generated by Django 5.0.1 on 2024-03-03 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vms_app', '0047_remove_fuel_master_fuel_time_fuel_master_fuel_date_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='fuel_master',
            new_name='FuelMaster',
        ),
    ]