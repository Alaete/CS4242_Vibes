# Generated by Django 3.0.5 on 2020-04-05 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Platform', '0004_auto_20200405_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vibe',
            name='topics',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]