# Generated by Django 4.0 on 2022-04-15 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_mycart_myproductcart'),
    ]

    operations = [
        migrations.AddField(
            model_name='mycart',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
    ]
