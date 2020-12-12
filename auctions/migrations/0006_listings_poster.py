# Generated by Django 3.1 on 2020-12-09 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20201209_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='poster',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_posts', to='auctions.user'),
            preserve_default=False,
        ),
    ]
