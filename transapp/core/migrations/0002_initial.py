# Generated by Django 4.0.5 on 2022-08-16 01:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='workplace',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workers', to='storage.warehouse'),
        ),
    ]
