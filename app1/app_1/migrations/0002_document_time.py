# Generated by Django 4.1 on 2022-09-11 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='time',
            field=models.TimeField(auto_now=True),
        ),
    ]
