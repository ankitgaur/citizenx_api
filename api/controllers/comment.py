from django.http import HttpResponse
from django.views import View
from django.conf import settings

import json, datetime, time

from ..models.comment import Comment as Model
from ..models.incident import Incident

class Comment(View):
	comment = Model()

	def get(self, request, *args, **kwargs):
		error = ''
		status = 200

		comment_data = {}

		if 'id' not in kwargs:
			error = 'Comment id is required'
			status = 400

		if not error:
			comment = Model.objects(id = kwargs['id'])

			if comment.count() <= 0:
				status = 404
				error = 'No record found'
			else:
				item = comment.first()

				comment_data['comment_id'] = str(item.id)
				comment_data['text'] = item.text
				comment_data['incident_id'] = str(item.incident_id)
				comment_data['incident_name'] = item.incident_name
				comment_data['user_id'] = str(item.user_id)
				comment_data['createdBy'] = item.user_name
				comment_data['createdOn'] = round(time.mktime(item.date_added.timetuple()))

		content = {
			'data': comment_data,
			'status': False if error else True,
			'error': error
		}

		return self.response(content, status_code = status)

	def put(self, request):
		error = None

		try:
			self.comment = Model()

			data = json.loads(request.body)

			if 'text' not in data or not data['text']:
				error = 'Comment text is required'
				status = 400

			if 'incident_id' not in data or not data['incident_id']:
				error = 'Incident ID is required'
				status = 400
			else:
				incident = Incident.objects(id = data['incident_id'])

				if incident.count() <= 0:
					error = 'Invalid Incident ID'
					status = 404
				else:
					incident = incident.first()

			if not error:
				self.comment.text = data['text']
				self.comment.incident_id = data['incident_id']
				self.comment.incident_name = incident['category']
				self.comment.user_id = request.session['user_id']
				self.comment.user_name = request.session['user_name']
				self.comment.date_added = datetime.datetime.now()
				self.comment.date_modified = datetime.datetime.now()

				self.comment.save()
		except Exception as e:
			error = str(e)
			status = 400

		content = {
			'error': error,
			'status': False if error else True,
			'id': str(self.comment)
		}

		return self.response(content, status_code = 200)

	def post(self, request, *args, **kwargs):
		error = ''
		status = 200

		try:
			data = json.loads(request.body)

			if 'id' not in kwargs:
				error = 'Comment id is required'
				status = 400
			else:
				comment = Model.objects(id = kwargs['id'])

				if comment.count() <= 0:
					status = 404
					error = 'No record found'

			if 'text' not in data and data['text']:
				error = 'Comment text is required'
				status = 400

			if not error:
				comment = comment.first()

				comment.text = data['text']
				comment.date_modified = datetime.datetime.now()

				comment.save()
		except Exception as e:
			error = str(e)
			status = 400

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
			error = 'Comment id is required'
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
