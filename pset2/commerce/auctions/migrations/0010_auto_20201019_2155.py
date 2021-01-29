# Generated by Django 3.1.2 on 2020-10-19 13:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_auto_20201012_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='Auction_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='auction',
            name='Auction_createdtime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='auction',
            name='Auction_photo',
            field=models.ImageField(default='AuctionPhotos/？？？.jpg', upload_to='AuctionPhotos'),
        ),
    ]