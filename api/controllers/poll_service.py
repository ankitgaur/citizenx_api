from django.http import HttpResponse
from django.views import View
from django.conf import settings

import json, datetime, time

from ..models.poll_service import PollService as Model

class PollService(View):
	poll_service = Model()

	def get(self, request, *args, **kwargs):
		error = ''
		status = 200

		poll_service_data = {}

		if 'id' not in kwargs:
			error = 'PollService id is required'
			status = 400

		if not error:
			poll_service = Model.objects(id = kwargs['id'])

			if len(poll_service) <= 0:
				status = 404
				error = 'No record found'

			for item in poll_service:
				poll_service_data['id'] = item.id
				poll_service_data['poll_id'] = item.id
				poll_service_data['poll_title'] = item.poll_title
				poll_service_data['poll_option'] = item.poll_option
				poll_service_data['poll_option_text'] = item.poll_option_text
				poll_service_data['createdBy'] = ''
				poll_service_data['createdOn'] = round(time.mktime(item.date_added.timetuple()))

		content = {
			'data': poll_service_data,
			'status': False if error else True,
			'error': error
		}

		return self.response(content, status_code = status)

	def put(self, request):
		data = json.loads(request.body)

		self.poll_service.poll_title = data['poll_title']
		self.poll_service.poll_option = data['poll_option']
		self.poll_service.poll_option_text = data['poll_option_text']
		self.poll_service.date_added = datetime.datetime.now()
		self.poll_service.date_modified = datetime.datetime.now()

		self.poll_service.save()

		content = {
			'error': None,
			'status': 200,
			'id': str(self.poll_service)
		}

		return self.response(content, status_code = 200)

	def post(self, request, *args, **kwargs):
		error = ''
		status = 200

		if 'id' not in kwargs:
			error = 'PollService id is required'
			status = 400

		if not error:
			poll_service = Model.objects(id = kwargs['id'])

			if len(poll_service) <= 0:
				status = 404
				error = 'No record found'
			else:
				poll_service = poll_service.first()
				data = json.loads(request.body)

				poll_service.poll_title = data['poll_title']
				poll_service.poll_option = data['poll_option']
				poll_service.poll_option_text = data['poll_option_text']
				poll_service.date_modified = datetime.datetime.now()

				poll_service.save()

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
			error = 'PollService id is required'
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
