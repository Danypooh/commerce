from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    starting_price = models.IntegerField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    end_date = models.DateTimeField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

class Bid(models.Model):
    auction_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid_amount = models.FloatField()
    bid_time = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    auction_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment_text = models.CharField(max_length=300)
    comment_time = models.DateTimeField(auto_now_add=True)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlists")

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'listing'], name='unique_user_listing')
        ]