# Generated by Django 4.0.5 on 2022-08-16 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, default=None, max_length=255, null=True, unique=True),
        ),
    ]
