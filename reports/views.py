from django.shortcuts import render, redirect
from django.conf import settings
from django.http.response import HttpResponseRedirect

from .forms.login import *
from .forms.register import *

from .models import User

import datetime, uuid, jwt

def index(request):
	error = ''

	success = request.session.get('success', '')

	if success:
		del request.session['success']

	if request.session.get('token', ''):
		return redirect_app(request.session['token'])

	if request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():
			user = User.objects(username = form.cleaned_data['username'], password = form.cleaned_data['password'])

			if user.count():
				user = user.first()
				request.session['token'] = str(jwt.encode({'user_id': str(user['id']), 'email': user['email'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds = settings.TOKEN_TTL)}, 'citizenx', algorithm='HS256'), 'utf-8')

				print('token', request.session['token'])

				return redirect_app(request.session['token'])
			else:
				error = 'Invalid username/password'
	else:
		form = LoginForm()

	return render(request, 'reports/index.html', {
		'form': form,
		'body_class': 'authentication-bg',
		'container_class' : 'account-pages mt-5 mb-5',
		'footer_class': 'footer-alt',
		'meta_title': 'Login',
		'error': error,
		'success': success
	})

def register(request):
	error = ''

	if request.session.get('token', ''):
		return redirect_app(request.session['token'])

	if request.method == 'POST':
		form = RegisterForm(request.POST)

		if form.is_valid():
			user = User.objects(username = form.cleaned_data['username'])

			if user.count():
				error = 'Already registered username'

			user = User.objects(email = form.cleaned_data['email'])

			if user.count():
				error = 'Already registered email id'

			if not error:
				user = User()

				user.name = form.cleaned_data['name']
				user.email = form.cleaned_data['email']
				user.username = form.cleaned_data['username']
				user.password = form.cleaned_data['password']
				user.date_added = datetime.datetime.now()
				user.date_modified = datetime.datetime.now()

				request.session['success'] = 'Account created, Please Login to use your account'

				user.save()

				return redirect('/')

	else:
		form = RegisterForm()

	return render(request, 'reports/register.html', {
		'form': form, 'body_class': 'authentication-bg',
		'container_class' : 'account-pages mt-5 mb-5',
		'footer_class': 'footer-alt',
		'error': error,
		'meta_title': 'Register'
	})

def logout(request):
	if request.session.get('token', ''):
		del request.session['token']

	return redirect('/')

def redirect_app(token):
	response = redirect(settings.REMOTE_APP + '#token=' + token)
	#response.set_cookie('token', token)
	response['token'] = token
	return response

def dashboard(request, token = None):
	return render(request, 'dashboard/index.html', {'request': request})
