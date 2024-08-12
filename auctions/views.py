from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages

from .models import User, Listing, Watchlist, Comment, Bid
from .forms import ListingForm


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


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
    
def new_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user # Set the seller to the authenticated user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForm()

    return render(request, "auctions/new_listing.html", {
        "form": form
    })

def view_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    item_in_watchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists()
    highest_bid = Bid.objects.filter(auction_listing=listing).order_by('-bid_amount').first()
    number_of_bids = listing.bids.count()
    message = "Messages will be displayed here"

    if request.method == "POST":
        action = request.POST.get('action')
        
        if action == "add":
            watchitem = Watchlist.objects.create(user=request.user, listing=listing)
            watchitem.save()
            item_in_watchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists()
            message = "Item added to watchlist"
                 
        elif action == "remove":
            Watchlist.objects.filter(user=request.user, listing=listing).delete()
            item_in_watchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists()
            message = "Item removed from watchlist"
        
        elif action == "place_bid":
            bid_str = request.POST.get('bid')
            if bid_str:
                try:
                    bid = float(bid_str)
                    if bid > 0:
                        if highest_bid is None and bid > listing.starting_price:
                            new_bid = Bid.objects.create(auction_listing=listing, bidder=request.user, bid_amount=bid, bid_time=timezone.now())
                            new_bid.save()
                            message = "Bid placed successfully"  
                            number_of_bids = listing.bids.count()
                            highest_bid = Bid.objects.filter(auction_listing=listing).order_by('-bid_amount').first()
                        elif highest_bid is not None and bid > highest_bid.bid_amount:
                            new_bid = Bid.objects.create(auction_listing=listing, bidder=request.user, bid_amount=bid, bid_time=timezone.now())
                            new_bid.save()
                            message = "Bid placed successfully"  
                            number_of_bids = listing.bids.count()
                            highest_bid = Bid.objects.filter(auction_listing=listing).order_by('-bid_amount').first()
                        else:
                            message = "Your bid must be higher than the current bid/price"
                    else:
                        message = "Bid amount must be greater than zero"
                except ValueError:
                        message = f"Invalid bid amount { highest_bid }"
        
        return render(request, 'auctions/view_listing.html', {
        'listing': listing,
        "item_in_watchlist": item_in_watchlist,
        "number_of_bids": number_of_bids,
        "highest_bid": highest_bid,
        "message": message
    })       

    return render(request, 'auctions/view_listing.html', {
        'listing': listing,
        "item_in_watchlist": item_in_watchlist,
        "number_of_bids": number_of_bids,
        "highest_bid": highest_bid,
        "message": message
    })