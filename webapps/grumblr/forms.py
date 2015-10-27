from django import forms
from django.core.validators import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.forms import ModelForm, Form
from django.forms.extras.widgets import SelectDateWidget
from grumblr.models import *
from django.contrib.auth.hashers import check_password

class RegistrationForm(Form):
	username = forms.CharField(max_length = 20, 
								widget=forms.TextInput())
	email = forms.EmailField(max_length = 200, 
								label='Email', 
								widget=forms.EmailInput())
	password1 = forms.CharField(max_length = 200, 
								label='Password', 
								widget = forms.PasswordInput())
	password2 = forms.CharField(max_length = 200, 
								label='Confirm password', 
								widget = forms.PasswordInput())


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
	def clean(self):
		# Calls our parent (forms.Form) .clean function, gets a dictionary
		# of cleaned data as a result
		cleaned_data = super(RegistrationForm, self).clean()

		# Confirms that the two password fields match
		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords did not match.")

		# We must return the cleaned data we got from our parent.
		return cleaned_data


    # Customizes form validation for the username field.
	def clean_username(self):
		# Confirms that the username is not already present in the
		# User model database.
		username = self.cleaned_data.get('username')
		if User.objects.filter(username__exact=username):
			raise forms.ValidationError("Username is already taken.")

		# We must return the cleaned data we got from the cleaned_data
		# dictionary
		return username

	def clean_email(self):
        # Confirms that the username is not already present in the
        # User model database.
		email = self.cleaned_data.get('email')
		if User.objects.filter(email__exact=email):
			raise forms.ValidationError("Email is already taken.")

		# We must return the cleaned data we got from the cleaned_data
		# dictionary
		return email

class EditProfileForm(ModelForm):
	class Meta:
		model = ProfileInfo
		fields = '__all__'
		exclude = ['user', 'email', 'following']
		labels = {
			'photo' : 'Upload a Profile Photo',
			'dob' : 'Date of Birth',
			'bio' : 'A little about yourself',
		}
		widgets = {
			'photo' : forms.FileInput(),
			'dob' : SelectDateWidget(years=range(1980, 2012)),
			'bio' : forms.Textarea(attrs={'class' : 'form-control', 'maxlength' : 420, 'placeholder' : '420 character limit'})
		}

class EditPasswordForm(Form):
	password1 = forms.CharField(label='New Password',
								required=False,
								widget=forms.PasswordInput())
	password2 = forms.CharField(label='Confirm New Password',
								required=False,
								widget=forms.PasswordInput())
			
	def clean(self):
		# Calls our parent (forms.Form) .clean function, gets a dictionary
		# of cleaned data as a result
		cleaned_data = super(EditPasswordForm, self).clean()

		# Confirms that the two password fields match
		password1 = cleaned_data.get('password1')
		password2 = cleaned_data.get('password2')
		if (not password1 or not password2):
			raise forms.ValidationError("New password fields are empty")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords did not match.")
		
		# We must return the cleaned data we got from our parent.
		return cleaned_data
		
class EditEmailForm(ModelForm):
	class Meta:
		model = ProfileInfo
		fields = ('email',)
		widgets = {
			'email': forms.TextInput(),
		}
	
	def clean_email(self):
		# Calls our parent (forms.Form) .clean function, gets a dictionary
		# of cleaned data as a result
		email = self.cleaned_data.get('email')

		#Checking if email is valid
		if GrumblrUser.objects.filter(email__exact=email):
			raise forms.ValidationError("Email is already taken.")
		try:
			validate_email(email)	
		except ValidationError:
			raise forms.ValidationError("Not a valid email.")
		# We must return the cleaned data we got from the cleaned_data
		return email
	
class PostForm(ModelForm):
	class Meta:
		model = Post
		fields = '__all__'
		exclude = ['timestamp', 'user']
		labels = {
			'text' : 'Post Content',
		}
		widgets = {
			'text' : forms.Textarea(attrs={'class': 'form-control', 'placeholder' : 'Enter your Grumbl'})
		}
		
	def clean(self):
		# Calls our parent (forms.Form) .clean function, gets a dictionary
		# of cleaned data as a result
		cleaned_data = super(PostForm, self).clean()

		# Confirms that the two password fields match
		text = cleaned_data.get('text')
		if text=='':
			raise forms.ValidationError("Enter Post")

		# We must return the cleaned data we got from our parent.
		return cleaned_data


class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = '__all__'
		exclude = ['timestamp', 'user', 'post']
		labels = {
			'comment' : 'Comment Content'
		}
		widgets = {
			'comment' : forms.Textarea(attrs={'placeholder':'Enter your comment', 'rows':2})
		}