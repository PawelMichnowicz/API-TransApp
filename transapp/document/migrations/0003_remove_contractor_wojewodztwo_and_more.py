# Generated by Django 4.0.5 on 2022-08-26 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0002_contractor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contractor',
            name='wojewodztwo',
        ),
        migrations.AddField(
            model_name='contractor',
            name='apartment_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='contractor',
            name='city',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='contractor',
            name='city_post',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='contractor',
            name='commune',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='contractor',
            name='district',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='contractor',
            name='end_date_activity',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contractor',
            name='province',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='contractor',
            name='silos_id',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='contractor',
            name='status_nip',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='contractor',
            name='street',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='contractor',
            name='street_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='contractor',
            name='type',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='contractor',
            name='zip_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
