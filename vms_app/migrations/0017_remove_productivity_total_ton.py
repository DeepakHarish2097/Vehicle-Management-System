# Generated by Django 5.0.1 on 2024-02-22 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("vms_app", "0016_alter_productivity_total_trip"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productivity",
            name="total_ton",
        ),
    ]
