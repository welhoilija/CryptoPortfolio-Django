# Generated by Django 4.0.1 on 2022-04-26 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('PriceAnalysis', '0004_price_pricechange'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('address', models.CharField(max_length=100, unique=True)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('holdings', models.ManyToManyField(to='PriceAnalysis.Holding')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
