# Generated by Django 4.1.7 on 2023-03-17 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0028_remove_products_category_remove_products_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_list',
            name='orginalprice',
            field=models.FloatField(default=0),
        ),
    ]