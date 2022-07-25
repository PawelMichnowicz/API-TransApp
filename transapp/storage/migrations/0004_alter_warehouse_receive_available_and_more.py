# Generated by Django 4.0.5 on 2022-07-25 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0003_remove_warehouse_receive_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouse',
            name='receive_available',
            field=models.ManyToManyField(blank=True, related_name='warehouse_receive', to='storage.timespan'),
        ),
        migrations.AlterField(
            model_name='warehouse',
            name='send_available',
            field=models.ManyToManyField(blank=True, related_name='warehouse_send', to='storage.timespan'),
        ),
    ]
