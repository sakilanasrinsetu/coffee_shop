# Generated by Django 3.2.6 on 2022-10-20 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0008_alter_foodorder_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodorderlog',
            name='on_the_way_time_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
