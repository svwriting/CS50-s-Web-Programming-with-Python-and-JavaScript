# Generated by Django 3.1.2 on 2020-10-12 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20201012_0152'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='Auction_Categorie',
            new_name='Auction_Category',
        ),
    ]