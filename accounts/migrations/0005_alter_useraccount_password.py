# Generated by Django 3.2.6 on 2022-09-13 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20220913_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='password',
            field=models.CharField(default='d', max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
    ]
