from django.http import HttpResponse
from django.views import View
from django.conf import settings

import json, datetime, time

from ..models.sentiment import Sentiment as Model
from ..models.incident import Incident

class Sentiment(View):
	sentiment = Model()

	def get(self, request, *args, **kwargs):
		error = ''
		status = 200

		sentiment_data = {}

		if 'id' not in kwargs:
			error = 'Sentiment id is required'
			status = 400

		if not error:
			sentiment = Model.objects(id = kwargs['id'])

			if sentiment.count() <= 0:
				status = 404
				error = 'No record found'
			else:
				item = sentiment.first()

				sentiment_data['sentiment_id'] = str(item.id)
				sentiment_data['sentiment'] = item.sentiment
				sentiment_data['incident_id'] = str(item.incident_id)
				sentiment_data['incident_name'] = item.incident_name
				sentiment_data['user_id'] = str(item.user_id)
				sentiment_data['createdBy'] = item.user_name
				sentiment_data['createdOn'] = round(time.mktime(item.date_added.timetuple()))

		content = {
			'data': sentiment_data,
			'status': False if error else True,
			'error': error
		}

		return self.response(content, status_code = status)

	def put(self, request):
		error = None
		status = 200

		try:
			self.sentiment = Model()

			data = json.loads(request.body)

			if 'sentiment' not in data or not data['sentiment']:
				error = 'Sentiment sentiment is required'
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
				self.sentiment.sentiment = data['sentiment']
				self.sentiment.incident_id = data['incident_id']
				self.sentiment.incident_name = incident['category']
				self.sentiment.user_id = request.session['user_id']
				self.sentiment.user_name = request.session['user_name']
				self.sentiment.date_added = datetime.datetime.now()
				self.sentiment.date_modified = datetime.datetime.now()
				self.sentiment.save()

		except Exception as e:
			error = str(e)
			status = 400

		content = {
			'error': error,
			'status': False if error else True,
			'id': str(self.sentiment)
		}

		return self.response(content, status_code = status)

	def post(self, request, *args, **kwargs):
		error = ''
		status = 200

		try:
			data = json.loads(request.body)

			if 'id' not in kwargs:
				error = 'Sentiment id is required'
				status = 400
			else:
				sentiment = Model.objects(id = kwargs['id'])

				if sentiment.count() <= 0:
					status = 404
					error = 'No record found'

			if 'sentiment' not in data and data['sentiment']:
				error = 'Sentiment sentiment is required'
				status = 400

			if not error:
				sentiment = sentiment.first()

				sentiment.sentiment = data['sentiment']
				sentiment.date_modified = datetime.datetime.now()
				sentiment.save()

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
			error = 'Sentiment id is required'
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
