# Generated by Django 4.0.5 on 2022-08-03 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0010_remove_receiveaction_warehouse_and_more_squashed_0022_remove_action_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouse',
            name='openning_time',
            field=models.ManyToManyField(blank=True, to='storage.openningtime'),
        ),
    ]
