# Generated by Django 4.0 on 2022-04-15 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_remove_mycart_user_mycart_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mycart',
            name='products',
        ),
        migrations.AddField(
            model_name='mycart',
            name='products',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='product_key', to='shop.myproduct'),
        ),
    ]
