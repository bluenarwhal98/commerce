# Generated by Django 3.1 on 2020-12-09 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listings_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='category',
            field=models.IntegerField(),
        ),
    ]
