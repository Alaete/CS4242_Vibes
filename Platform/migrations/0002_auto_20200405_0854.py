# Generated by Django 3.0.5 on 2020-04-05 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Platform', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revibe',
            name='edited_at',
            field=models.DateTimeField(default=None),
        ),
        migrations.AlterField(
            model_name='vibe',
            name='edited_at',
            field=models.DateTimeField(default=None),
        ),
    ]