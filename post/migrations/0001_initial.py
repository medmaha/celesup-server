# Generated by Django 4.1.5 on 2023-04-03 00:15

from django.db import migrations, models
import post.picture_model


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, default='default/photo.png', null=True, upload_to=post.picture_model.post_photo_path)),
                ('alt_text', models.CharField(default='post by', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('key', models.CharField(blank=True, max_length=100, primary_key=True, serialize=False)),
                ('publish', models.CharField(default='Public', max_length=35)),
                ('caption', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('excerpt', models.TextField(blank=True, default='', max_length=2000, null=True)),
                ('hashtags', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('activity_rate', models.BigIntegerField(blank=True, default=1, null=True)),
            ],
            options={
                'ordering': ('-updated_at', 'activity_rate', '-created_at'),
                'get_latest_by': 'created_at',
            },
        ),
    ]
