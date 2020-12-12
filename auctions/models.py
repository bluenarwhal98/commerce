from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
	poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
	name = models.CharField(max_length=64)
	description = models.TextField()
	category = models.CharField(max_length=64)
	start_bid = models.IntegerField()
	image_url = models.URLField()
	active = models.BooleanField()

	def __str__(self):
		return f"{self.name}: {self.description} \n \n Starting bid: {self.start_bid}"

class Bids(models.Model):
	bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
	bidded_item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids")
	bid_amount = models.IntegerField()

	def __str__(self):
		return f"{self.bidder} has bidded {self.bid_amount} on {self.bidded_item}"

class Comments(models.Model):
	item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comments")
	commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
	comment = models.TextField()

	def __str__(self):
		return f"{self.commenter} says: {self.comment}" 

class Watchlist(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="on_watcb")
	item = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="watchers")

	def __str__(self):
		return f"{self.user} places {self.item} on the watchlist"
