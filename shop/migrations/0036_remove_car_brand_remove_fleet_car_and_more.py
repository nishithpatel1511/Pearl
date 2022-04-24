# Generated by Django 4.0 on 2022-04-24 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0035_brand_car_alter_myvariance_category_fleet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='brand',
        ),
        migrations.RemoveField(
            model_name='fleet',
            name='car',
        ),
        migrations.AlterField(
            model_name='myvariance',
            name='category',
            field=models.CharField(choices=[('package', 'package'), ('size', 'size'), ('color', 'color')], default='size', max_length=25),
        ),
        migrations.AlterUniqueTogether(
            name='myproductvariant',
            unique_together={('product', 'variant_type')},
        ),
        migrations.DeleteModel(
            name='Brand',
        ),
        migrations.DeleteModel(
            name='Car',
        ),
        migrations.DeleteModel(
            name='Fleet',
        ),
    ]
