# Generated by Django 4.0.5 on 2022-08-04 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0012_alter_warehouse_openning_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouse',
            name='openning_time',
            field=models.ManyToManyField(blank=True, to='storage.openningtime'),
        ),
    ]
