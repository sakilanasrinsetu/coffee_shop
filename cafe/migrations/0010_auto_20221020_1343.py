# Generated by Django 3.2.6 on 2022-10-20 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0009_foodorderlog_on_the_way_time_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='cafe',
        ),
        migrations.AddField(
            model_name='notification',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='notification'),
        ),
    ]
