# Generated by Django 4.0.5 on 2022-08-26 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regon', models.CharField(max_length=14)),
                ('nip', models.CharField(max_length=14)),
                ('nazwa', models.CharField(max_length=100)),
                ('wojewodztwo', models.CharField(max_length=20)),
            ],
        ),
    ]
