# Generated by Django 4.2.6 on 2023-11-03 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_product_downloads'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='usd_price',
            field=models.DecimalField(decimal_places=2, default=80, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]