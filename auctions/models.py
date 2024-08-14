from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint

# Define category choices
CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('home', 'Home & Garden'),
        ('toys', 'Toys & Games'),
        ('sports', 'Sports & Outdoors'),
        ('books', 'Books & Media'),
        ('vehicles', 'Vehicles'),
        ('art', 'Art')
    ]

class User(AbstractUser):
    pass

class Categorie(models.Model):
    name = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='art'
    )

    def __str__(self):
        return self.name

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    starting_price = models.FloatField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    end_date = models.DateTimeField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    status = models.BooleanField(default=True)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name="items", blank=True, null=True)
    
    def __str__(self):
        return self.title

class Bid(models.Model):
    auction_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid_amount = models.FloatField()
    bid_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bid_amount

class Comment(models.Model):
    auction_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment_text = models.CharField(max_length=300)
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_text

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlists")

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'listing'], name='unique_user_listing')
        ]
    
    def __str__(self):
        return self.listing
