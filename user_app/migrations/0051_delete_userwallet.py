# Generated by Django 4.1.7 on 2023-03-13 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0050_userwallet_delete_wallet'),
    ]

    operations = [
        migrations.DeleteModel(
            name='userwallet',
        ),
    ]