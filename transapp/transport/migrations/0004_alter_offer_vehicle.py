# Generated by Django 4.0.5 on 2022-07-27 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0003_offer_accepted_offer_vehicle_alter_offer_id_offer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='vehicle',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='transport.vehicle'),
        ),
    ]