from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Listings, Bids, Comments, Watchlist


def index(request):
    if request.method =="POST":
    #Gather all necessary information on listing
        name = request.POST["name"]
        #Redirect to List_page function
        return HttpResponseRedirect(reverse('list_page', args=(name,)))
        

    else:
        #If GET: Render Active Listings Page 
        return render(request, "auctions/index.html", {"Listings": Listings.objects.filter(active=True)})

def list_page(request, name):
    username = request.user.username 
    user = User.objects.filter(username=username)[0:1].get()
    selected_item = Listings.objects.get(name=name)
    comment = selected_item.comments
    comment_count = comment.count()
    bids = selected_item.bids 
    poster = selected_item.poster
    poster_name = poster.username 
    #Find highest current bid, if non-existent bid is set at 0
    try:
        highest_bid = bids.order_by("bid_amount")[0:1].get()
    except ObjectDoesNotExist:
        highest_bid = 0
    #Determine if user already made item on their watchlist
    if not request.user:
        waka = False
    else:
        try:
            temp = Watchlist.objects.filter(user=user).filter(item=selected_item).get()
            waka = True
        except ObjectDoesNotExist:
            waka = False
    #If relevant, determine if user has won the bid
    if selected_item.active == False:
        user_bid = Bids.objects.get(bidder=user, bidded_item=selected_item)
        if user_bid.bid_amount >= highest_bid.bid_amount:
            win_or_not = True
        else:
            win_or_not = False
    else:
        win_or_not = False

    return render(request, "auctions/item.html", {"Item": selected_item, "Comments": comment.all(), "Count": comment_count, "Highest_Bid": highest_bid, "Waka": waka, "Poster_Name": poster_name, "Win": win_or_not})


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

def list(request):
    if request.method == "POST":
        #Fix information into relevant database "Listings"
        username = request.user.username 
        user = User.objects.filter(username=username)[0:1].get()
        listing = Listings()
        listing.poster = user
        listing.name = request.POST["name"]
        listing.description = request.POST["desp"]
        listing.start_bid = request.POST["bid"]
        if not request.POST["category"]:
            listing.category = "Others"
        else:
            listing.category = request.POST["category"]

        if not request.POST["img"]:
           listing.image_url = "//upload.wikimedia.org/wikipedia/commons/0/0a/No-image-available.png"
        else:  
            listing.image_url = request.POST["img"]
        listing.active = True
        listing.save()
        #redirect to active listings page
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/list.html")

def category_list(request):
    return render(request, "auctions/category.html")

def category(request, category):
    result = Listings.objects.filter(category=category)
    return render(request, "auctions/result.html", {"Result": result,"Count":result.count()})



def bid(request):
    #Extract information from HTML
    bid = request.POST["bid"]
    item_id = request.POST["item_id"]
    username = request.user.username 
    user = User.objects.filter(username=username)[0:1].get()
    item = Listings.objects.get(id=item_id)
     #check if user already made a bid on the item before
    #if so, create new entry
    if not Bids.objects.filter(bidder=user).filter(bidded_item=item):
        bidding = Bids(bidder=user, bidded_item=item, bid_amount=bid)
        bidding.save()
    else:
        #if not, update existing record
        bidding = Bids.objects.filter(bidder=user).filter(bidded_item=item).get()
        bidding.bid_amount = bid
        bidding.save()
    #return to index page
    return HttpResponseRedirect(reverse("index"))

def comment(request):
    #Extract infromation from HTML
    comment = request.POST["comment"]
    item_id = request.POST["item_id"]
    #add comment to database
    username = request.user.username 
    user = User.objects.filter(username=username)[0:1].get()
    item = Listings.objects.get(id=item_id)
    commenting = Comments(item=item, commenter=user, comment=comment)
    commenting.save()
    #return to index page
    return HttpResponseRedirect(reverse("index"))

def watchlist(request):
    if request.method == "POST":
        #Reference to relevant item and user database entries and save into Watchlist Database
        username = request.user.username 
        user = User.objects.filter(username=username)[0:1].get()
        item_id = request.POST["item_id"]
        listing = Listings.objects.filter(id=item_id).get()

        watchlist = Watchlist(user=user, item=listing)
        watchlist.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        #load up watchlist page
        username = request.user.username 
        user = User.objects.filter(username=username)[0:1].get()
        watchlist = Watchlist.objects.filter(user=user).all()

        return render(request, "auctions/watchlist.html", {"Watchlist": watchlist})

def remove_watchlist(request):
    if request.method == "POST":
        #Identify watchlist item and remove
        username = request.user.username 
        user = User.objects.filter(username=username)[0:1].get()
        item_id = request.POST["item_id"]
        listing = Listings.objects.filter(id=item_id).get()
        watchlist = Watchlist.objects.filter(user=user).filter(item=listing).get()
        watchlist.delete()

        return HttpResponseRedirect(reverse("index"))

def my_listing(request):
    if request.method == "POST":
        #Remove listing from active 
        item_id = request.POST["item_id"]
        listing = Listings.objects.get(id=item_id)
        listing.active = False
        listing.save()

        return HttpResponseRedirect(reverse("my_listing"))

    else:
        #find all current listings made by user
        username = request.user.username 
        user = User.objects.filter(username=username)[0:1].get()

        return render(request, "auctions/my_listing.html", {"Listing": Listings.objects.filter(poster=user)})

def delete(request, id_num):
    if request.method == "POST":
        #Remove list from database
        listing = Listings.objects.get(id=id_num)
        listing.delete()

        return HttpResponseRedirect(reverse("my_listing"))
        






