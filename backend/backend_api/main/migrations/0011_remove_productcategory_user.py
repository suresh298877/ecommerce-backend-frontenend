# Generated by Django 4.2.6 on 2023-10-13 04:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_rename_customer_productrating_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productcategory',
            name='user',
        ),
    ]