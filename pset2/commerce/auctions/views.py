from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import *
import django_resized

@csrf_exempt
def index(request,categoryTag_=None,auctionId_=None):
    AuctionsHTML_="<h2>Active Listings</h2>"
    if auctionId_: # Detail
        auction_=Auction.objects.get(id=auctionId_)
        bids_=Bid.objects.filter(Bid_Auction=auctionId_).order_by('-Bid_price')
        if len(bids_)>0:
            iscurrentbid=(bids_[0].Bid_User.username==request.user.username)
            price_=bids_[0].Bid_price
        else:
            iscurrentbid=False
            price_=auction_.Auction_startingbid
        if request.method=='POST':
            if 'comment' in request.POST:
                comment_=Comment(
                    Comment_User=request.user,
                    Comment_Auction=auction_,
                    Comment_content=request.POST['comment'],
                )
                comment_.save()
            elif request.POST['POSTQ']=='CLOSE':
                auction_.Auction_active=False
                auction_.save()
            elif request.POST['POSTQ']=='Watchlist':
                User_=User.objects.get(id=request.user.id)
                if User_.User_watchlist and auction_ not in User_.User_watchlist.all():
                    User_.User_watchlist.add(auction_)
                else :
                    User_.User_watchlist.remove(auction_)
                User_.save()
            elif request.POST['POSTQ']=='Place Bid':
                temp_bid = Bid(
                    Bid_User=User.objects.get(id=request.user.id),
                    Bid_Auction=Auction.objects.get(id=auctionId_),
                    Bid_price=request.POST['bidprice']
                )
                temp_bid.save()
                price_=request.POST['bidprice']
                bids_=Bid.objects.filter(Bid_Auction=auctionId_).order_by('-Bid_price')
        if request.user.User_watchlist and auction_ in request.user.User_watchlist.all():
            isInWatchList_=True
        else:
            isInWatchList_=False
        if auction_.Auction_User==request.user:
            isyours=True
        else:
            isyours=False
        #auction_.Auction_title
        AuctionDetailHTML_="<h2>"+auction_.Auction_title+"</h2>"
        #isInWatchList_
        AuctionDetailHTML_+="<form method='post'><input type='submit' id='WLButton' style='border-radius:10px;color:white;outline:0;"
        if isInWatchList_:
            AuctionDetailHTML_+="background-color:rgb(13, 123, 255);'"
        else:
            AuctionDetailHTML_+="background-color:gray;'"
        AuctionDetailHTML_+=" value='Watchlist' name='POSTQ'></form>"
        #auction_.Auction_photo
        AuctionDetailHTML_+="<img src='Django/media/"+str(auction_.Auction_photo)+"' style='max-width:500px;max-height:400px;' >"
        #auction_.Auction_description
        AuctionDetailHTML_+="<br/><label >"+auction_.Auction_description+"</label>"
        #price_
        AuctionDetailHTML_+="<h3>$"+str(price_)+"</h3>"
        #iscurrentbid
        if auction_.Auction_active:
            #isyours
            if isyours:
                AuctionDetailHTML_+="<form method='post'><input type='submit' name='POSTQ' value='CLOSE' onclick='javascript:return confirm()'></form>"
            AuctionDetailHTML_+="<label >"+str(len(bids_))+(" bids" if len(bids_)>1 else " bid") +" so far. "
            if iscurrentbid:
                AuctionDetailHTML_+="Your bid is the current bid. "
            AuctionDetailHTML_+="</label>"
            # Place Bid
            if request.user.is_authenticated:
                AuctionDetailHTML_+="<form method='post'>"
                #AuctionDetailHTML_+="<div style='width:210px;border-style:solid;border-color:silver;' >"
                AuctionDetailHTML_+="<script>function bidCheck_t(form){ \
                    if( form.bidprice.value!='' && (Number(form.bidprice.value) >" + ('=' if len(bids_)<=0 else '') + str(price_)+")){\
                        document.getElementById('warringlabel').style.display = 'none';\
                        document.getElementById('submitbutton').disabled=false;\
                    }else{ \
                        document.getElementById('warringlabel').style.display = 'block';\
                        document.getElementById('submitbutton').disabled=true;\
                    }}</script>"
                AuctionDetailHTML_+="<input id='bidprice' name='bidprice' type='text' pattern='[0-9]{1,14}(\.{0,1}[0-9]{1,2})?' placeholder='Bid$' required \
                    onkeyup='bidCheck_t(this.form);'>"
                #AuctionDetailHTML_+="</div>"
                AuctionDetailHTML_+="<input id='submitbutton' type='submit' name='POSTQ' value='Place Bid' disabled>"
                AuctionDetailHTML_+="<label id='warringlabel' style='color:red;display:none;' >  Your bid must be"
                if len(bids_)>0:
                    AuctionDetailHTML_+=" greater than"
                else:
                    AuctionDetailHTML_+=" at least as large as"
                AuctionDetailHTML_+=" $"+str(price_)+".</label></form>"
        else:
            AuctionDetailHTML_+="<label style='color:red;'>The auction is closed."
            if iscurrentbid:
                AuctionDetailHTML_+=" You won!"
            AuctionDetailHTML_+="</label>"
        # Details
        AuctionDetailHTML_+="<h4>Details</h4>"
        #User.objects.get(username=auction_.Auction_User.username)
        AuctionDetailHTML_+="<ul><li>Listed by:"
        AuctionDetailHTML_+="<a href='createdby="+auction_.Auction_User.username+"'>"+auction_.Auction_User.username+"</a>"
        #auction_.Auction_Category
        AuctionDetailHTML_+="</li><li>Category:"
        AuctionDetailHTML_+="<a href='"+auction_.Auction_Category.Category_title+"'>"+auction_.Auction_Category.Category_title+"</a>"
        #auction_.Auction_createdtime
        AuctionDetailHTML_+="</li><li>Created: "
        AuctionDetailHTML_+=auction_.Auction_createdtime.strftime('%Y-%m-%d %H:%M:%S')
        AuctionDetailHTML_+="</li></ul>"
        # Comments
        AuctionDetailHTML_+="<h4>Comments</h4>"
        if request.user.is_authenticated:
            AuctionDetailHTML_+='<form method="post"><input type="text" name="comment" maxlength="64" style="outline:0px;font-weight: normal;width: 400px;border: 1px solid #ccc;border-radius: 4px;box-sizing: border-box;padding: 6px 8px;min-height: 36px;font-size: 14px;flex: 1 1 auto;max-width: 100%;" required>'
            AuctionDetailHTML_+="<input type='submit' value='Comment'></form>"
        comments_=Comment.objects.filter(Comment_Auction=auction_).order_by('-Comment_datetime')
        for comment_ in comments_:
            AuctionDetailHTML_+="<hr><label style='font-weight:bold;'>"+comment_.Comment_User.username+"：</label>"
            AuctionDetailHTML_+="<label>"+comment_.Comment_content+"</label>"
            AuctionDetailHTML_+="<label style='font-size:12px;position:absolute;left:400px;color:gray;'>Created "+comment_.Comment_datetime.strftime('%Y-%m-%d %H:%M:%S')+"</label>"
        return render(request, "auctions/index.html",{
            'HTML':AuctionDetailHTML_
        })
    else:
        allCategories_=[ Category.Category_title for Category in Category.objects.all()]
        if categoryTag_==None:
            categoryTag_=='ALL'
            CategoryTag=False
        else:
            CategoryTag=True
        if categoryTag_=='ALL' or  categoryTag_ not in allCategories_:
            categorys_=set(Category.objects.all())
        else:
            categorys_=set([Category.objects.get(Category_title=categoryTag_)])
        if CategoryTag:
            allCategories_.append('ALL')
            allCategories_="".join([" <a href='"+str_+"' style='font-weight:bold;'>"+str_+"</a> ," if str_!=categoryTag_ else \
                                " <a href='"+str_+"' style='font-weight:bold;background-color:navajowhite;border-radius:5px;'>"+str_+"</a> ," \
                                for str_ in allCategories_ ])
            AuctionsHTML_+="<div style=''>"+allCategories_[:-2]+"</div>"
        for category_ in categorys_:
            AuctionsHTML_+=HTMLList(Auction.objects.filter(Auction_active=True).filter(Auction_Category=category_),CategoryTag=CategoryTag)
        return render(request, "auctions/index.html",{
            'HTML':AuctionsHTML_
        })

def indexU(request,username_):
    AuctionsHTML_="<h2>Active Listings</h2>"
    AuctionsHTML_="<h4>Listed by "+username_+"</h4>"
    AuctionsHTML_+=HTMLList(Auction.objects.filter(Auction_User=User.objects.get(username=username_)).order_by('Auction_active'),ActiveTag=True,CategoryTag=False)
    return render(request, "auctions/index.html",{
        'HTML':AuctionsHTML_
    })

def HTMLList(Auctions_,ActiveTag=False,CategoryTag=True):
    strHTML_=""
    for Auction_ in Auctions_:
        strHTML_+="<div style='display:grid;grid-template-columns:200px 400px;height:210px;border-style:solid;'>"
        strHTML_+="<div>"
        if Auction_.Auction_photo.width>Auction_.Auction_photo.height:
            wd=0
            hd=206-200*Auction_.Auction_photo.height/Auction_.Auction_photo.width
        else:
            hd=6
            wd=200-200*Auction_.Auction_photo.width/Auction_.Auction_photo.height
        strHTML_+="<img src='Django/media/"+str(Auction_.Auction_photo)+"' style='max-width:200px;max-height:200px;margin-left:"+str(wd/2)+"px;margin-top:"+str(hd/2)+"px;' >"
        strHTML_+="</div>"
        strHTML_+="<div style='border-left-style:double;height:205px;position:relative;'/>"
        strHTML_+="<a href='../Detail/"+str(Auction_.Auction_id)+"' style='font-weight:bold;color:black;font-size:30px;margin-left:15px;'>"+Auction_.Auction_title+"</a>"
        if ActiveTag:
            strHTML_+="<label style='font-size:8px;color:red;'> "+ ("" if Auction_.Auction_active else "Closed!")+"</label>"
        strHTML_+="<br/>"
        bids_=Bid.objects.filter(Bid_Auction=Auction_.Auction_id).order_by('-Bid_price')
        if len(bids_)>0:
            strHTML_+="<label style='margin-left:20px;'>Price: $"+str(bids_[0].Bid_price)+"</label><br/>"
        else:
            strHTML_+="<label style='margin-left:20px;'>Price: $0 </label><br/>"
        strHTML_+="<label style='font-size:12px;margin-left:20px;color:gray;'>Created "+Auction_.Auction_createdtime.strftime('%Y-%m-%d %H:%M:%S')+"</label>"
        if CategoryTag:
            strHTML_+="<a href='"+Auction_.Auction_Category.Category_title+"' style='text-decoration:underline;font-style:italic;font-size:8px;margin-left:20px;position:absolute;bottom:20px;left:0px;'>"+Auction_.Auction_Category.Category_title+"</a>"
        strHTML_+="</div>"
        strHTML_+="</div>"
    return strHTML_

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def detail(request,auctionId_):
    return HttpResponseRedirect(reverse("indexD",args={auctionId_}))

def watchlist(request):
    tempHTML=HTMLList(request.user.User_watchlist.all(),ActiveTag=True,CategoryTag=False)
    if tempHTML=="":
        tempHTML="<h1 style='text-align:center;' > - Empty - </h1>"
    tempHTML="<h2>Watchlist</h2>"+tempHTML
    return render(request, "auctions/index.html",{
        'HTML':tempHTML
    })

@csrf_exempt
def create(request):
    if request.method == "POST":
        temp_auction = Auction(
            Auction_title=request.POST['Auction_title'],
            Auction_description=request.POST['Auction_description'],
            Auction_photo=request.FILES['Auction_photo'],
            Auction_Category=Category.objects.get(id=request.POST['Auction_Category']),
            Auction_User=request.user,
            Auction_startingbid=request.POST['Auction_startingbid'] if request.POST['Auction_startingbid']!=None else 0
        )
        print(request.FILES['Auction_photo'])
        temp_auction.save()
        return HttpResponseRedirect(reverse("detail",args={Auction.objects.all()[::-1][0].Auction_id}))
    else:
        categorys_=[ category_ for category_ in Category.objects.all()]
        selectItemsHTML="<option value='1' selected=''>"+str(categorys_[0].Category_title)+"</option>"
        for i in range(1,len(categorys_)):
            selectItemsHTML+="<option value='"+str(categorys_[i].id)+"' >"+categorys_[i].Category_title+"</option>"
        return render(request, "auctions/create.html",{
            'selectItems':selectItemsHTML
        })

@csrf_exempt
def addcategory(request):
    if request.method=='POST':
        if request.POST['Category_title'] not in [category_.Category_title for category_ in Category.objects.all()]:
            temp_category = Category(
                Category_title=request.POST['Category_title']
            )
            temp_category.save()
            selectit_=Category.objects.filter(Category_title=request.POST['Category_title'])[0].Category_title
            selecti_=Category.objects.filter(Category_title=request.POST['Category_title'])[0].id
            return HttpResponse('<script type="text/javascript">window.opener.document.getElementById("sss").options.add(new Option("'+selectit_+'","'+str(selecti_)+'")); window.opener.document.getElementById("sss").value="'+str(selecti_)+'" ; window.close();</script>')
        else:
            selecti_=Category.objects.filter(Category_title=request.POST['Category_title'])[0].id
            return HttpResponse('<script type="text/javascript">window.opener.document.getElementById("sss").value="'+str(selecti_)+'" ; window.close();</script>')
    else:
        return render(request,"auctions/addcategory.html")



