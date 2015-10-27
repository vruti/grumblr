from django.db import models
import datetime, sys

#Using user from built-in django authetication module
from django.contrib.auth.models import User

# Create your models here.
#The user profile class
#Contains basic user information
class ProfileInfo(models.Model):
	user = models.ForeignKey(User)
	email = models.EmailField(blank = True)
	photo = models.ImageField(upload_to='/media/images', default='/static/images/no-image.png')
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	dob = models.DateTimeField(blank=True, null=True)
	bio = models.CharField(max_length=430, blank=True)
	following = models.ManyToManyField('self', 
	                                   related_name='followedUsers', 
									   symmetrical=False)
	def __str__(self):
		return self.user.username

#The post class
#Foreign key is the user creating the post
class Post(models.Model):
	text = models.CharField(max_length=300)
	user = models.ForeignKey(ProfileInfo, related_name='posts')
	timestamp = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.text
		
	class Meta:
		ordering = ('-id',)
		
#The comment class, foreign key being the post that
#the comment is being made on
class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, related_name="comment")
	user = models.ForeignKey(ProfileInfo)
	comment = models.CharField(max_length=300)
	timestamp = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return comment