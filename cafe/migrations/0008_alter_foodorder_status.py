# Generated by Django 3.2.6 on 2022-10-17 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0007_alter_foodorder_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodorder',
            name='status',
            field=models.CharField(choices=[('ORDER_PLACED', 'Order Confirm'), ('PREPARING', 'Preparing'), ('PICKED', 'Picked Up'), ('ON_THE_WAY', 'On the Way'), ('DELIVERED', 'Delivered'), ('INVOICE', 'Invoice'), ('CANCELLED', 'Cancelled')], default='USER_CONFIRMED', max_length=50),
        ),
    ]
