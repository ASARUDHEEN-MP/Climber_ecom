# Generated by Django 4.1.4 on 2023-01-29 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0004_category_status'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='Categorys',
        ),
        migrations.RenameModel(
            old_name='product',
            new_name='products',
        ),
        migrations.RenameField(
            model_name='products',
            old_name='category',
            new_name='Categorys',
        ),
    ]
