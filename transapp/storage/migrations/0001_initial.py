# Generated by Django 4.0.5 on 2022-07-25 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenningTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_hour', models.TimeField()),
                ('to_hour', models.TimeField()),
                ('weekday', models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Timedelta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_hour', models.TimeField()),
                ('to_hour', models.TimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Timespan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_hour', models.TimeField()),
                ('to_hour', models.TimeField()),
                ('month_day', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openning_time', models.ManyToManyField(to='storage.openningtime')),
                ('receive_time', models.ManyToManyField(related_name='warehouse_receive', to='storage.timespan')),
                ('send_time', models.ManyToManyField(related_name='warehouse_send', to='storage.timespan')),
            ],
        ),
        migrations.CreateModel(
            name='SendAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_delta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='storage.timedelta')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.warehouse')),
                ('workers', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReceiveAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_delta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='storage.timedelta')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.warehouse')),
                ('workers', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
