# Generated by Django 4.2.6 on 2023-11-01 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_orderitems_price_orderitems_qty'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.BooleanField(default=False),
        ),
    ]