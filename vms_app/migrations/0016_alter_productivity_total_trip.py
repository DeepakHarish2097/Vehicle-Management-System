# Generated by Django 5.0.1 on 2024-02-21 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vms_app', '0015_rename_rounds_productivity_fifth_trip_ton_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productivity',
            name='total_trip',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
