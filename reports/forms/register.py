from django import forms

class RegisterForm(forms.Form):
	name = forms.CharField(max_length=254)
	username = forms.CharField(max_length=254)
	email = forms.CharField(widget=forms.EmailInput)
	password = forms.CharField(widget=forms.PasswordInput)
