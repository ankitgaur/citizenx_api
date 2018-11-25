from django.http import HttpResponse
from django.views import View
from django.conf import settings

import json, datetime, time, uuid, jwt

from ..models.user import User as Model

class User(View):
	user = Model()

	def get(self, request, *args, **kwargs):
		error = ''
		status = 200

		user_data = {}

		if request.session.get('user_id', ''):
			user = Model.objects(id = request.session['user_id'])

			if user.count() == 0:
				status = 404
				error = 'No record found'
			else:
				item = user.first()

				user_data['name'] = item.name
				user_data['email'] = item.email
				user_data['username'] = item.username
				user_data['createdOn'] = round(time.mktime(item.date_added.timetuple()))
		else:
			error = 'Please login first'

		content = {
			'data': user_data,
			'status': False if error else True,
			'error': error
		}

		return self.response(content, status_code = status)

	def put(self, request):
		error = ''
		status = 200

		try:
			data = json.loads(request.body)

			user = Model.objects(username = data['username'])

			if user.count():
				error = 'Already registered username'

			user = Model.objects(email = data['email'])

			if user.count():
				error = 'Already registered email id'

			if not error:
				user = Model()

				user.name = data['name']
				user.email = data['email']
				user.username = data['username']
				user.password = data['password']
				user.date_added = datetime.datetime.now()
				user.date_modified = datetime.datetime.now()

				request.session['success'] = 'Account created, Please Login to use your account'

				user.save()
		except Exception as e:
			error = str(e)
			status = 400

		content = {
			'data': {},
			'status': False if error else True,
			'error': error
		}

		return self.response(content, status_code = 200)

	def post(self, request, *args, **kwargs):
		error = ''
		token = ''
		status = 200
		data = []

		try:
			data = json.loads(request.body)

			if 'username' not in data or 'password' not in data:
				error = 'Invalid username/password'
			else:
				user = Model.objects(username = data['username'], password = data['password'])

				if user.count():
					user = user.first()
					token = str(jwt.encode({'user_id': str(user['id']), 'email': user['email'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds = settings.TOKEN_TTL)}, 'citizenx', algorithm='HS256'), 'utf-8')

					print('token', token)
				else:
					error = 'Invalid username/password'
		except Exception as e:
			error = str(e)
			status = 400

		content = {
			'data': token,
			'status': False if error else True,
			'error': error
		}

		return self.response(content, status_code = status)

	def delete(self, request, *args, **kwargs):
		error = 'This method is not allowed'
		status = 400

		content = {
			'data': {},
			'status': False if error else True,
			'error': error
		}

		return self.response(content, status_code = status)

	def response(self, data, status_code = 200):
		httpresponse = HttpResponse(json.dumps(data), content_type = 'application/json')
		httpresponse.status_code = status_code

		return httpresponse
