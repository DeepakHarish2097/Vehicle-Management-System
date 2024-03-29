# Generated by Django 5.0.1 on 2024-03-26 17:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vms_app', '0055_jobcard_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicles_RTO_details',
            fields=[
                ('vehicle', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='vms_app.vehicle')),
                ('chassis_number', models.CharField(blank=True, max_length=50, null=True)),
                ('vehicle_model', models.CharField(blank=True, max_length=50, null=True)),
                ('vehicle_type', models.CharField(blank=True, max_length=50, null=True)),
                ('engine_number', models.CharField(blank=True, max_length=50, null=True)),
                ('fc_date', models.DateField(blank=True, null=True)),
                ('insurance', models.DateField(blank=True, null=True)),
                ('puc', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='route',
            old_name='street',
            new_name='route',
        ),
        migrations.RenameField(
            model_name='transferregister',
            old_name='transfer_date',
            new_name='request_date',
        ),
        migrations.RenameField(
            model_name='triphistory',
            old_name='trip_load',
            new_name='total_trip_load',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='chassis_number',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='engine_number',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='fc_date',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='insurance',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='puc',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='register_number',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='vehicle_model',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='vehicle_type',
        ),
        migrations.AddField(
            model_name='route',
            name='starting_point',
            field=models.CharField(blank=True, default=None, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='transferregister',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='emp_responds', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transferregister',
            name='approved_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='transferregister',
            name='remark',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='transferregister',
            name='status',
            field=models.CharField(choices=[('approved', 'approved'), ('hold', 'hold'), ('rejected', 'rejected')], default='hold', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='triphistory',
            name='dry_waste',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='triphistory',
            name='green_garbages',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='triphistory',
            name='household_hazard',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='triphistory',
            name='inerts',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='triphistory',
            name='other_waste',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='triphistory',
            name='recyclable_waste',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='triphistory',
            name='wet_waste',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='current_route',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='routesofvehicle', to='vms_app.route'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='is_spare',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='transferregister',
            name='requested_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='emp_requests_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
