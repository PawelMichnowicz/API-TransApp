# Generated by Django 4.0.5 on 2022-07-25 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0001_initial'),
        ('core', '0002_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='warehouse',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workers', to='storage.warehouse'),
        ),
        migrations.AlterField(
            model_name='user',
            name='position',
            field=models.CharField(choices=[('USR', 'User'), ('WHR', 'Warehouser'), ('DIR', 'Director')], default='USR', max_length=3),
        ),
    ]
