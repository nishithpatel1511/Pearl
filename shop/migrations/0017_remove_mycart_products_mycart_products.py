# Generated by Django 4.0 on 2022-04-15 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_remove_mycart_products_mycart_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mycart',
            name='products',
        ),
        migrations.AddField(
            model_name='mycart',
            name='products',
            field=models.ManyToManyField(blank=True, null=True, to='shop.myProduct'),
        ),
    ]
