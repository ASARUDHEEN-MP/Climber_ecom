# Generated by Django 4.1.7 on 2023-03-09 08:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0042_orderitem_discountprice'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='discountprice',
            new_name='total',
        ),
    ]
