from django.http import HttpResponse
from django.views import View
from django.conf import settings

import json, datetime, time

from ..models.state import State as Model

class State(View):
	incident = Model()

	def get(self, request, *args, **kwargs):
		error = ''
		status = 200
		state_data = []

		states = Model.objects()

		for item in states:
			state_data.append({
				'id'	: str(item['id']),
				'name'	: item['name']
			})

		content = {
			'data': state_data,
			'status': False if error else True,
			'error': error
		}

		return self.response(content, status_code = status)

	def put(self, request):
		error = 'This method is not allowed'
		status = 400

		content = {
			'data': {},
			'status': False if error else True,
			'error': error
		}

		return self.response(content, status_code = status)

	def post(self, request, *args, **kwargs):
		error = 'This method is not allowed'
		status = 400

		content = {
			'data': {},
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
