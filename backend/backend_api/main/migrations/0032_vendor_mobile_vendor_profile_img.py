# Generated by Django 4.2.6 on 2023-11-06 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_alter_customeraddress_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='mobile',
            field=models.PositiveBigIntegerField(null=True, unique=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='profile_img',
            field=models.ImageField(null=True, upload_to='seller_imgs/'),
        ),
    ]
