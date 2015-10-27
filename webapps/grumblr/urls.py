"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = [
    url(r'^grumblr$', 'grumblr.views.main'),
	url(r'^$', 'grumblr.views.main'),
	url(r'^profile/(?P<p_user>\w+)$', 'grumblr.views.view_profile', name='profile'),
	url(r'^edit-profile/$', 'grumblr.views.edit_profile', name='edit-profile'),
	url(r'^edit-password/$', 'grumblr.views.edit_password', name='edit-password'),
	url(r'^edit-email/$', 'grumblr.views.edit_password', name='edit-email'),
	url(r'^register$', 'grumblr.views.register', name='register'),
	url(r'^new-post$','grumblr.views.add_new', name='new-post'),
	url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
	url(r'^follow/(?P<p_user>\w+)$', 'grumblr.views.follow', name='follow'),
	url(r'^unfollow/(?P<p_user>\w+)$', 'grumblr.views.unfollow', name='unfollow'),
	url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'grumblr/login.html'}),
	url(r'^reset-password$', 'django.contrib.auth.views.password_reset', {'post_reset_redirect' : 'reset-password/sent/'}, name='reset-password'),
	url(r'^reset-password/sent/$', 'django.contrib.auth.views.password_reset_done'),
	url(r'^reset-password/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : 'reset-password/done/'}),
    url(r'^reset-password/done/$', 
        'django.contrib.auth.views.password_reset_complete'),
	url(r'^get-posts/(?P<post_id>\d+)$', 'grumblr.views.get_stream', name='get-stream'),
	url(r'^add-comment/(?P<post_id>\d+)$', 'grumblr.views.add_comment', name='add-comment'),
	url(r'^get-comments/(?P<post_id>\d+)$', 'grumblr.views.get_comments', name='get-comments')
	]
