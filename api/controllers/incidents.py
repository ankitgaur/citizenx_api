from django.http import HttpResponse
from django.views import View
from django.conf import settings

import json, datetime, time

from ..models.incident import Incident as Model

class Incident(View):
	incident = Model()

	def get(self, request, *args, **kwargs):
		error = ''
		status = 200

		incident_data = {}

		if 'id' not in kwargs:
			error = 'Incident id is required'
			status = 400

		if not error:
			incident = Model.objects(id = kwargs['id'])

			if len(incident) <= 0:
				status = 404
				error = 'No record found'

			item = incident.first()

			incident_data['category'] = item.category
			incident_data['subcategory'] = item.subcategory
			incident_data['country'] = item.country
			incident_data['state'] = item.state
			incident_data['city'] = item.city
			incident_data['questions'] = item.questions
			incident_data['rating'] = item.rating
			incident_data['description'] = item.description
			incident_data['createdOn'] = round(time.mktime(item.date_added.timetuple()))

		content = {
			'data': incident_data,
			'status': False if error else True,
			'error': error
		}

		return self.response(content, status_code = status)

	def put(self, request):
		error = None
		status = 200

		try:
			data = json.loads(request.body)

			self.incident.category = data['category']
			self.incident.subcategory = data['subcategory']
			self.incident.country = data['country']
			self.incident.state = data['state']
			self.incident.city = data['city']
			self.incident.questions = data['questions']
			self.incident.rating = data['rating']
			self.incident.description = data['description']
			self.incident.date_added = datetime.datetime.now()
			self.incident.date_modified = datetime.datetime.now()
			self.incident.save()
			
		except Exception as e:
			error = str(e)
			status = 400

		content = {
			'error': error,
			'status': False if error else True,
			'id': str(self.incident)
		}

		return self.response(content, status_code = status)

	def post(self, request, *args, **kwargs):
		error = ''
		status = 200

		try:
			data = json.loads(request.body)

			if 'id' not in kwargs:
				error = 'Incident id is required'
				status = 400
			else:
				incident = Model.objects(id = kwargs['id'])

				if len(incident) <= 0:
					status = 404
					error = 'No record found'
				else:
					incident = incident.first()

			if not error:
				incident.category = data['category']
				incident.subcategory = data['subcategory']
				incident.country = data['country']
				incident.state = data['state']
				incident.city = data['city']
				incident.questions = data['questions']
				incident.rating = data['rating']
				incident.description = data['description']
				incident.date_modified = datetime.datetime.now()
				incident.save()

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
			error = 'Incident id is required'
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
