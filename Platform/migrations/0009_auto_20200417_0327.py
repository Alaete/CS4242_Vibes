# Generated by Django 3.0.5 on 2020-04-17 03:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Platform', '0008_delete_thread'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='revibe',
            name='views',
        ),
        migrations.RemoveField(
            model_name='vibe',
            name='views',
        ),
    ]
