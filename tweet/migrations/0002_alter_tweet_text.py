# Generated by Django 5.1.4 on 2025-01-13 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='text',
            field=models.TextField(max_length=500),
        ),
    ]
