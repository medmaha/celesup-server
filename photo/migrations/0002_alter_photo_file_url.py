# Generated by Django 4.1.5 on 2023-04-03 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file_url',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
