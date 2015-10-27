from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.mail import send_mail
from django.contrib.auth.models import User

from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.utils import formats
from grumblr.models import *
from grumblr.forms import *
from django.http import HttpResponse
import logging, json

# Create your views here.

@login_required
def main(request):
	user_info = get_object_or_404(ProfileInfo, user=request.user)
	following = user_info.following.all()
	
	#Get all the posts from the users being followed by current user 
	#Ordered by newest first
	posts = []
	for followed in following:
		posts = list(chain(posts, follwed.post_user.all().order_by('-timestamp')))

	#Sending posts and comment form to add to posts
	context = {'posts' : posts, 'form': CommentForm() }
	return render(request, 'grumblr/globalstream.html', context)

@login_required
def get_stream(request, post_id):
	user_info = get_object_or_404(ProfileInfo, user=request.user)
	following = user_info.following.all()
	posts = []
	
	#If no posts displayed, then get all possible posts
	if(post_id == 0):
		for followed in following:
			posts = list(chain(posts, follwed.post_user.all().order_by('-timestamp')))
	else:
		#get only new posts
		for followed in following:
			posts = list(chain(posts, follwed.post_user.all().filter(id__gt=post_id).order_by('-timestamp')))
	
	context = {'posts' : posts}
	return render(request, 'grumblr/globalstream.html', context)
	
@login_required
def view_profile(request, p_user):
	user_info = get_object_or_404(ProfileInfo, user=request.user)
	#User who's profile current user is visiting
	p_user_obj = get_object_or_404(User, username=p_user)
	p_user_info = get_object_or_404(ProfileInfo, user=p_user_obj)
	
	#If 
	own_page = request.user.username == p_user
	followed = False
	if(own_page):
		#So that current user can view their own posts
		followed = True
	else:
		#Check if current user is following the other uer
		if(user_info.following.all().filter(user=p_user_obj)):
			followed = True

	#All the users being followed by visited user
	following = p_user_info.following.all();
	#All posts by visited user in order of newest first
	posts = Post.objects.filter(user=p_user_info).order_by('-timestamp')
	context = {'info' : p_user_info, 
				'posts' : posts, 
				'own_page' : own_page, 
				'following' : following,
				'user':request.user.username,
				'p_user' : p_user,
				'followed' : followed,
				 'form': CommentForm() 
				}
	return render(request, 'grumblr/profile.html', context)

#To follow a user
@login_required
def follow(request, p_user):
	user = get_object_or_404(User, username=p_user)
	user_info = get_object_or_404(ProfileInfo, user=user)
	ru_profile = get_object_or_404(ProfileInfo, user=request.user)
	ru.following.add(user_info)
	ru_profile.save()
	
	return view_profile(request, p_user)
	
#To unfollow a user
@login_required
def unfollow(request, p_user):
	user = get_object_or_404(User, username=p_user)
	user_info = get_object_or_404(ProfileInfo, user=user)
	ru_profile = get_object_or_404(ProfileInfo, user=request.user)
	ru_profile.following.remove(user_info)
	ru_profile.save()
	
	return view_profile(request, p_user)
	
@login_required
def edit_profile(request):
	user_info = get_object_or_404(ProfileInfo, user=request.user)
	context= {}
	
	#Display form if page is just loading
	if request.method == 'GET':
		context['form'] = EditProfileForm(instance=user_info);
		return render(request, 'grumblr/edit-profile.html', context)
	
	form = EditProfileForm(request.POST, request.FILES, instance=user_info)
	context['form'] = form
	
	#If input isn't valid, just reset page
	if (not form.is_valid()):
		return render(request, 'grumblr/edit-profile.html', context)
	
	#Saving all the fields changed
	form.save()
	
	return view_profile(request, request.user.username)

@login_required
def edit_password(request):
	user_info = get_object_or_404(ProfileInfo, user=request.user)
	context = {}
	
	#Display form if page is just loading
	if request.method == 'GET':
		context['form'] = EditPasswordForm()
		return render(request, 'grumblr/edit-password.html', context)
	
	
	form = EditPasswordForm(request.POST)
	context['form'] = form
	
	#If input isn't valid, just reset page
	if not form.is_valid():
		return render(request, 'grumblr/edit-password.html', context)
		
	#Saving new password
	new_password = form.cleaned_data['password1']
	request.user.password = make_password(new_password)
	request.user.save()
	
	user = authenticate(username=request.user, password=new_password)
	login(request, user)
	
	return view_profile(request, request.user.username)
	
@login_required
def add_new(request):
	context={}

	#Display form if page is just loading
	if request.method == 'GET':
		context['form'] = PostForm()
		return render(request, 'grumblr/new-post.html', context)
	
	post_form = PostForm(request.POST)
	context['form'] = PostForm()
	
	#If input isn't valid, just reset page
	if(not post_form.is_valid()):
		return render(request, 'grumblr/new-post.html', context)
		
	#Adding new post
	user_info = get_object_or_404(ProfileInfo, user=request.user)
	new_post = Post(user = user_info, text= post_form.cleaned_data['text'])
	new_post.save()
	return main(request)

def register(request):
	context = {}

	# Just display the registration form if this is a GET request
	if request.method == 'GET':
		context['form'] = RegistrationForm()
		return render(request, 'grumblr/register.html', context)

	# Creates a bound form from the request POST parameters and makes the 
	# form available in the request context dictionary.
	form = RegistrationForm(request.POST)
	context['form'] = form

	# Validates the form.
	if not form.is_valid():
		return render(request, 'grumblr/register.html', context)

	# Creates the new user from the valid form data
	new_user = User.objects.create_user(username=form.cleaned_data['username'], \
										password=form.cleaned_data['password1'], \
										email=form.cleaned_data['email'])
	new_user.save()

	# Logs in the new user and redirects to his/her feed
	new_user = authenticate(username=request.POST['username'], \
							password=request.POST['password1'])

	new_info = ProfileInfo(user = new_user, email=form.cleaned_data['email'])
	new_info.save()

	login(request, new_user)
	return redirect('/grumblr/edit-profile')


@login_required
def add_comment(request, post_id):
	comment_form = CommentForm(request.POST)
	post = get_object_or_404(Post, id=post_id)
	user_info = get_object_or_404(ProfileInfo, user=request.user)
	
	#If input isn't valid, just ignore and get new comments
	if(not comment_form.is_valid()):
		return get_comments(request, post_id)
	
	#Adding new comment and sending it to be displayed
	newComment = Comment(user = user_info, post= post, comment=comment_form.cleaned_data['comment'])
	newComment.save()
	
	return get_comments(request, post_id)
	
@login_required
def get_comments(request, post_id):
	post = get_object_or_404(Post, id=post_id)
	#picking out all new comments to be displayed
	comments = []
	comment_data = Comment.objects.filter(post=post)
	for comment in comment_data:
		comments.append({'comment': comment.comment, 'timestamp':formats.date_format(comment.timestamp, "DATETIME_FORMAT")})
		
	return HttpResponse(json.dumps(comments), content_type="application/json")