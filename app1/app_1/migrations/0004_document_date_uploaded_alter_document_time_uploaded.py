# Generated by Django 4.1 on 2022-09-12 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0003_rename_time_document_time_uploaded'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='date_uploaded',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='time_uploaded',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
