# Generated by Django 3.1.2 on 2020-10-19 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auto_20201019_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='Auction_Category',
            field=models.ForeignKey(default=2, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='AuctionCategory_id', to='auctions.category'),
        ),
    ]
