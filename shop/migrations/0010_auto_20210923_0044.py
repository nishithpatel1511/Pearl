# Generated by Django 3.2.5 on 2021-09-22 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20210917_1122'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=25)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='has_color',
            field=models.BooleanField(default='False'),
        ),
        migrations.CreateModel(
            name='ProductImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='', upload_to='')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ProductImages', to='shop.product')),
            ],
        ),
    ]