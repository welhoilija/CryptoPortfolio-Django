# Generated by Django 4.0.1 on 2022-03-25 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PriceAnalysis', '0003_rename_price_price_last_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='pricechange',
            field=models.DecimalField(decimal_places=5, default=None, max_digits=8, null=True),
        ),
    ]
