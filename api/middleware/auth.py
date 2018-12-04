from django.conf import settings
from django.http import HttpResponse

from ..models.user import User

import json, jwt

class Auth:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		if request.META['REQUEST_METHOD'] != 'GET' and request.path.find('/api/') != -1 and request.path.find('/login/') == -1 and request.path.find('/register/') == -1:
			# Token validation is here

			payload = {}

			if  request.META['REQUEST_METHOD'] == 'OPTIONS':
				return self.response({
					'status': True,
					'error': '',
				})

			if 'HTTP_TOKEN' in request.META:
				try:
					payload = jwt.decode(request.META['HTTP_TOKEN'], 'citizenx', leeway=10, algorithm='HS256')
				except jwt.InvalidTokenError:
					return self.authenticationFailure(msg = 'Invalid token')
				except jwt.ExpiredSignatureError:
					return self.authenticationFailure(msg = 'Token is expired')

			print('Auth Payload', payload)

			if len(payload) == 0 or 'user_id' not in payload or 'email' not in payload:
				return self.authenticationFailure()
			else:
				user = User.objects(id = payload['user_id'], email = payload['email'])

				if not user.count():
					return self.authenticationFailure()
				else:
					user = user.first()
					request.session['user_id'] = str(user['id'])
					request.session['user_name'] = str(user['name'])

		response = self.get_response(request)

		response["Access-Control-Allow-Origin"] = "*"
		response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
		response["Access-Control-Max-Age"] = "1000"
		response["Access-Control-Allow-Headers"] = "Content-Type, token"

		return response

	def authenticationFailure(self, msg = 'Unauthorized', other = {}):
		if other:
			return self.response({
				'status': False,
				'other': other,
				'error': msg,
			}, status_code = 401)
		else:
			return self.response({
				'status': False,
				'error': msg,
			}, status_code = 401)

	def response(self, data, status_code = 200):
		httpresponse = HttpResponse(json.dumps(data), content_type = 'application/json')
		httpresponse.status_code = status_code
		httpresponse["Access-Control-Allow-Origin"] = "*"
		httpresponse["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
		httpresponse["Access-Control-Max-Age"] = "1000"
		httpresponse["Access-Control-Allow-Headers"] = "Content-Type, token"

		return httpresponse
