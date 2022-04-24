# Generated by Django 4.0 on 2022-04-24 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0029_vehicle_myproduct_catefory_car'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myproduct',
            name='catefory',
        ),
        migrations.AlterField(
            model_name='myproduct',
            name='category',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.mycategory'),
        ),
        migrations.AlterField(
            model_name='myvariance',
            name='category',
            field=models.CharField(choices=[('color', 'color'), ('size', 'size'), ('package', 'package')], default='size', max_length=25),
        ),
    ]
