# Generated by Django 4.1.7 on 2023-03-16 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0053_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Out_for_delivery', 'Out_for_delivery'), ('Confirmed', 'Confirmed'), ('Shipped', 'Shipped'), ('Pending', 'Pending'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled'), ('Returned', 'Returned'), ('Refund', 'Refund')], default='pending', max_length=30),
        ),
    ]
