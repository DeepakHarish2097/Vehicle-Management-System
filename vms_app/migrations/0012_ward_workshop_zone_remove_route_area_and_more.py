# Generated by Django 5.0.1 on 2024-02-21 06:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vms_app', '0011_route_supervisor_alter_productivity_routes_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ward_name', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workshop_name', models.CharField(max_length=50)),
                ('incharge', models.CharField(blank=True, max_length=50, null=True)),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zone_name', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField()),
            ],
        ),
        migrations.RemoveField(
            model_name='route',
            name='area',
        ),
        migrations.RemoveField(
            model_name='route',
            name='block',
        ),
        migrations.AddField(
            model_name='vehicle',
            name='chassis_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='engine_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='fc_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='insurance',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='puc',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='register_number',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='vehicle_model',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='AccidentLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver_name', models.CharField(max_length=50)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('employee_id', models.CharField(blank=True, max_length=50, null=True)),
                ('contact', models.CharField(blank=True, max_length=50, null=True)),
                ('accident_time', models.DateTimeField(blank=True, null=True)),
                ('accident_location', models.CharField(blank=True, max_length=250, null=True)),
                ('accident_severity', models.CharField(choices=[('Fatality', 'Fatality'), ('Near Miss', 'Near Miss'), ('Property Damage', 'Property Damage')], max_length=100)),
                ('cause_of_accident', models.CharField(choices=[('Mechanical Failure', 'Mechanical Failure'), ('Hydraulic Failure', 'Hydraulic Failure'), ('Over Speeding', 'Over Speeding'), ('Poor Visibility', 'Poor Visibility'), ('Lack of Attention', 'Lack of Attention'), ('Influence of Alcohol', 'Influence of Alcohol'), ('Lack of Training', 'Lack of Training'), ('Others', 'Others')], max_length=100)),
                ('action_needed', models.TextField()),
                ('remark', models.TextField()),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vms_app.vehicle')),
            ],
        ),
        migrations.AddField(
            model_name='route',
            name='ward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ward_routes_set', to='vms_app.ward'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='workshop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='workshop_vehicles_set', to='vms_app.workshop'),
        ),
        migrations.AddField(
            model_name='ward',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contained_wards_set', to='vms_app.zone'),
        ),
        migrations.CreateModel(
            name='TransferRegister',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transferred_date', models.DateField()),
                ('reason', models.TextField()),
                ('log_no', models.PositiveIntegerField(blank=True, null=True)),
                ('requested_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vms_app.vehicle')),
                ('from_zone', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='from_zones_tl', to='vms_app.zone')),
                ('to_zone', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='to_zones_tl', to='vms_app.zone')),
            ],
        ),
        migrations.AddField(
            model_name='route',
            name='zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='zone_routes_set', to='vms_app.zone'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='zone_vehicles_set', to='vms_app.zone'),
        ),
    ]
