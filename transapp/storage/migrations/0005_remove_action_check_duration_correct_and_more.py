# Generated by Django 4.0.5 on 2022-08-27 14:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('storage', '0004_action_check_duration_correct'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='action',
            name='check_duration_correct',
        ),
        migrations.AlterField(
            model_name='action',
            name='action_window',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='action', to='storage.actionwindow'),
        ),
        migrations.AlterField(
            model_name='action',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='storage.warehouse'),
        ),
        migrations.AlterField(
            model_name='action',
            name='workers',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='action',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('duration__isnull', False), ('status', 'delivered')), models.Q(('duration__isnull', False), ('status', 'delivered_broken')), models.Q(('duration__isnull', True), ('status', 'in_progress')), models.Q(('duration__isnull', True), ('status', 'unready')), _connector='OR'), name='check_duration_correct'),
        ),
    ]