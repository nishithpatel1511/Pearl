# Generated by Django 4.0 on 2022-05-21 19:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0048_remove_cartitemvariant_item_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItemVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.cartitem')),
            ],
        ),
    ]