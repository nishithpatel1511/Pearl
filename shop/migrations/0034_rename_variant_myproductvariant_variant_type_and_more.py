# Generated by Django 4.0 on 2022-04-24 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0033_remove_myproductvariant_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myproductvariant',
            old_name='variant',
            new_name='variant_type',
        ),
        migrations.RemoveField(
            model_name='myproductvariant',
            name='value',
        ),
        migrations.AddField(
            model_name='myproductvariant',
            name='unit',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='myvariance',
            name='category',
            field=models.CharField(choices=[('package', 'package'), ('color', 'color'), ('size', 'size')], default='size', max_length=25),
        ),
        migrations.CreateModel(
            name='myProductVariantValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=25)),
                ('variant_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.myproductvariant')),
            ],
        ),
    ]
