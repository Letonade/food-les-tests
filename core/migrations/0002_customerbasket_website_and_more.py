# Generated by Django 4.2.18 on 2025-01-24 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerBasket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='productpalette',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_palettes', to='core.warehouse'),
        ),
        migrations.CreateModel(
            name='WebsiteProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
                ('website', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='website_products', to='core.website')),
            ],
            options={
                'unique_together': {('website', 'product')},
            },
        ),
        migrations.AddField(
            model_name='website',
            name='products',
            field=models.ManyToManyField(related_name='websites', through='core.WebsiteProduct', to='core.product'),
        ),
        migrations.AddField(
            model_name='website',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='websites', to='core.warehouse'),
        ),
        migrations.CreateModel(
            name='CustomerBasketProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basket_products', to='core.customerbasket')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
            ],
            options={
                'unique_together': {('basket', 'product')},
            },
        ),
        migrations.AddField(
            model_name='customerbasket',
            name='products',
            field=models.ManyToManyField(related_name='customer_baskets', through='core.CustomerBasketProduct', to='core.product'),
        ),
        migrations.AddField(
            model_name='customerbasket',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_baskets', to='core.warehouse'),
        ),
    ]
