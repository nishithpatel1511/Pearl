# Generated by Django 4.0 on 2022-04-24 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0025_mycategory_alter_myvariance_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='myproduct',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='myproductcategory', to='shop.mycategory'),
        ),
        migrations.AlterField(
            model_name='myvariance',
            name='category',
            field=models.CharField(choices=[('package', 'package'), ('color', 'color'), ('size', 'size')], default='size', max_length=25),
        ),
    ]
