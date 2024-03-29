# Generated by Django 4.1.7 on 2023-03-17 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0027_alter_products_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='category',
        ),
        migrations.RemoveField(
            model_name='products',
            name='image',
        ),
        migrations.RemoveField(
            model_name='products',
            name='is_published',
        ),
        migrations.RemoveField(
            model_name='products',
            name='name',
        ),
        migrations.RemoveField(
            model_name='products',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='products',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='products',
            name='status',
        ),
        migrations.AddField(
            model_name='product_list',
            name='discountprice',
            field=models.FloatField(default=0),
        ),
    ]
