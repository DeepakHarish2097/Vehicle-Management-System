# Generated by Django 5.0.1 on 2024-02-24 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vms_app', '0025_productivity_created_date_productivity_created_on_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='productivity',
            unique_together={('shift', 'vehicle', 'created_date', 'out_km')},
        ),
    ]
