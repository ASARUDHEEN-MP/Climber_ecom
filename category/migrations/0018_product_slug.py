# Generated by Django 4.1.5 on 2023-01-31 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0017_product_is_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.CharField(default='SOME STRING', max_length=140),
        ),
    ]
