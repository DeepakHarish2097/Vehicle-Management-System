# Generated by Django 5.0.1 on 2024-02-04 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vms_app', '0005_merge_20240204_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='productivity',
            name='rounds',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
