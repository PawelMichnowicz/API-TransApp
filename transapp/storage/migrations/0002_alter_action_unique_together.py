# Generated by Django 4.0.5 on 2022-08-23 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='action',
            unique_together={('action_id', 'status')},
        ),
    ]