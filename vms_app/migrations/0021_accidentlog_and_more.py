# Generated by Django 5.0.1 on 2024-02-24 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vms_app', '0020_delete_maintanencehistory'),
    ]

    operations = [
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
            ],
        ),
        migrations.RemoveField(
            model_name='transferregister',
            name='accident_location',
        ),
        migrations.RemoveField(
            model_name='transferregister',
            name='accident_severity',
        ),
        migrations.RemoveField(
            model_name='transferregister',
            name='accident_time',
        ),
        migrations.RemoveField(
            model_name='transferregister',
            name='action_needed',
        ),
        migrations.RemoveField(
            model_name='transferregister',
            name='age',
        ),
        migrations.RemoveField(
            model_name='transferregister',
            name='cause_of_accident',
        ),
        migrations.RemoveField(
            model_name='transferregister',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='transferregister',
            name='driver_name',
        ),
        migrations.RemoveField(
            model_name='transferregister',
            name='employee_id',
        ),
        migrations.RemoveField(
            model_name='transferregister',
            name='remark',
        ),
    ]
