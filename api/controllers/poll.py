from django.http import HttpResponse
from django.views import View
from django.conf import settings

import json, datetime, time

from ..models.poll import Poll as Model

class Poll(View):
	poll = Model()

	def get(self, request, *args, **kwargs):
		error = ''
		status = 200

		poll_data = {}

		if 'id' not in kwargs:
			error = 'Poll id is required'
			status = 400

		if not error:
			poll = Model.objects(id = kwargs['id'])

			if len(poll) <= 0:
				status = 404
				error = 'No record found'

			for item in poll:
				poll_data['title'] = item.category
				poll_data['options'] = item.options

		content = {
			'data': poll_data,
			'status': False if error else True,
			'error': error
		}

		return self.response(content, status_code = status)

	def put(self, request):
		data = json.loads(request.body)

		self.poll.title = data['title']
		self.poll.options = data['options']
		self.poll.date_added = datetime.datetime.now()
		self.poll.date_modified = datetime.datetime.now()

		self.poll.save()

		content = {
			'error': None,
			'status': 200,
			'id': str(self.poll)
		}

		return self.response(content, status_code = 200)

	def post(self, request, *args, **kwargs):
		error = ''
		status = 200

		if 'id' not in kwargs:
			error = 'Poll id is required'
			status = 400

		if not error:
			poll = Model.objects(id = kwargs['id'])

			if len(poll) <= 0:
				status = 404
				error = 'No record found'
			else:
				poll = poll.first()
				data = json.loads(request.body)

				poll.title = data['title']
				poll.options = data['options']
				poll.date_modified = datetime.datetime.now()

				poll.save()

		content = {
			'data': None,
			'status': False if error else True,
			'error': error
		}

		return self.response(content, status_code = status)

	def delete(self, request, *args, **kwargs):
		error = ''
		status = 200

		if 'id' not in kwargs:
			error = 'Poll id is required'
			status = 400

		if not error:
			Model.objects(id = kwargs['id']).delete()

		content = {
			'data': None,
			'status': False if error else True,
			'error': error
		}

		return self.response(content, status_code = status)

	def response(self, data, status_code = 200):
		httpresponse = HttpResponse(json.dumps(data), content_type = 'application/json')
		httpresponse.status_code = status_code

		return httpresponse
