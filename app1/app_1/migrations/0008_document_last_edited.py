# Generated by Django 4.1 on 2022-09-15 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0007_remove_document_pdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='last_edited',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]