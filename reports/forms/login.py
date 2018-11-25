from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(max_length=254)
	password = forms.CharField(widget=forms.PasswordInput)
