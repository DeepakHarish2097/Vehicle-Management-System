# Generated by Django 5.0.1 on 2024-03-03 04:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vms_app', '0050_rename_fuel_quantiry_fuelmaster_fuel_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fuelmaster',
            old_name='fuel_Date',
            new_name='fuel_date',
        ),
    ]
