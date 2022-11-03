# Generated by Django 3.2.6 on 2022-10-01 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_useraccount_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='last_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='email',
            field=models.EmailField(max_length=35, unique=True),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='phone',
            field=models.CharField(blank=True, max_length=35, null=True),
        ),
    ]
