# Generated by Django 3.0.5 on 2020-04-05 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Platform', '0003_auto_20200405_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revibe',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='vibe',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
