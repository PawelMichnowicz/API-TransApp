# Generated by Django 4.0.5 on 2022-08-22 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='broken',
            field=models.BooleanField(default=False),
        ),
    ]
