from django.db import models
from django_resized import ResizedImageField

#1
class Category(models.Model):
    Category_title=models.CharField(max_length=64, unique=True)
    @property
    def Category_id(self):
       return self.id

#2
class Bid(models.Model):
    Bid_User=models.ForeignKey('User',on_delete=models.CASCADE,related_name='BidUser_id')
    Bid_Auction=models.ForeignKey('Auction',on_delete=models.CASCADE,related_name='BidAuction_id')
    Bid_price=models.DecimalField(max_digits=12,decimal_places=2)

#3
class Comment(models.Model):
    Comment_User=models.ForeignKey('User',on_delete=models.SET_NULL,null=True,related_name='CommentUser_id')
    Comment_Auction=models.ForeignKey('Auction',on_delete=models.CASCADE,related_name='CommentAuction_id')
    Comment_content=models.TextField(max_length=200)
    Comment_datetime=models.DateTimeField(auto_now=True)

#4
class Auction(models.Model):
    Auction_title=models.CharField(max_length=64)
    Auction_description=models.TextField(max_length=200)
    Auction_photo=models.ImageField(upload_to='AuctionPhotos',default='AuctionPhotos/？？？.jpg')
    # Auction.Auction_photo.save('name.png',  File(open('path_to_pic/image.png', 'rb'))
    Auction_Category=models.ForeignKey('Category',on_delete=models.SET_NULL,null=True,default=1,related_name='AuctionCategory_id')
    Auction_User=models.ForeignKey('User',on_delete=models.SET_NULL,null=True,related_name='AuctionUser_id')
    Auction_createdtime=models.DateTimeField(auto_now_add=True)
    Auction_active =models.BooleanField(default=True)
    Auction_startingbid=models.IntegerField(default=0)
    @property
    def Auction_id(self):
       return self.id

#5
class User(AbstractUser):
    User_watchlist=models.ManyToManyField(Auction)
    def __str__(self):
       return f"{self.username}'s WatchList:"+str(self.User_watchlist)
