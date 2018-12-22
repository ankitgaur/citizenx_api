from django.http import HttpResponse
from django.views import View
from django.conf import settings

import json, datetime, time

from ..models.incident import Incident as Model

class IncidentFilter(View):
	incident = Model()

	def get(self, request, *args, **kwargs):
		error = 'This method is not allowed'
		status = 400

		content = {
			'data': {},
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
		error = ''
		total = 0
		status = 200

		incident_data = []
		daterang = {}

		if not error:
			filter = {}

			data = json.loads(request.body)

			print('Applying Filters on data ', data)

			if 'category' in data:
				filter['category__iexact'] = data['category']

			if 'subcategory' in data:
				filter['subcategory__iexact'] = data['subcategory']

			if 'state' in data:
				filter['state__iexact'] = data['state']

			if 'date_range' in data:
				explode = data['date_range'].split('-')

				if len(explode) > 1:
					print('Filtering date range', datetime.datetime.fromtimestamp(round(int(explode[0]) / 1000)), datetime.datetime.fromtimestamp(round(int(explode[1]) / 1000)))

					#filter['date_added'] = {
					daterang = {
						'$lte': datetime.datetime.fromtimestamp(round(int(explode[0]) / 1000)),
						'$gte': datetime.datetime.fromtimestamp(round(int(explode[1]) / 1000))
					}

			print('Filtering incidents', filter)

			if 'sort' in data:
				if 'order' in data and data['order'] == 'desc':
					data['sort'] = '-' + data['sort']

				incidents = Model.objects(**filter).order_by(data['sort'])
			else:
				incidents = Model.objects(**filter)

			if 'distinct' in data and 'groupby' not in data:
				incidents = incidents.distinct(data['distinct'])

			if 'groupby' in data:
				groupby = {}

				groupby['total'] = { '$sum': 1 }

				if 'distinct' in data and len(data['distinct']) > 0:
					groupby['distinct_value'] = { '$addToSet': '$' + data['distinct'] }

				if data['groupby'] == 'day':
					groupby['_id'] = {
						'make': '$make',
						'createdOn': {
							'$dateToString': {
								'format': '%Y-%m-%d',
								'date': '$date_added'
							}
						}
					}

					pipeline = [
						{
							'$match': {
								'date_added': daterang
							}
						},
						{
							'$group': groupby
						},
						{
							'$sort': { 'total': -1 }
						}
					]
				elif data['groupby'] == 'month':
					groupby['_id'] = {
						'make': '$make',
						'createdMonthYear': {
							'$dateToString': {
								'format': '%Y-%m',
								'date': '$date_added'
							}
						}
					}

					pipeline = [
						{
							'$match': {
								'date_added': daterang
							}
						},
						{
							'$group': groupby
						},
						{
							'$sort': { 'total': -1 }
						}
					]
				else:
					groupby['_id'] = '$' + data['groupby']

					pipeline = [
						{
							'$group': groupby
						},
						{
							'$sort': { 'total': -1 }
						}
					]

				print('Group By', pipeline)

				incidents = incidents.aggregate(*pipeline)

				for item in incidents:
					incident_data.append({
						data['groupby']: item['_id'] if '_id' in item else '',
						'distinct_value': item['distinct_value'] if 'distinct_value' in item else [],
						'total': item['total'] if 'total' in item else 0,
					})

			#print('Mongo Query', incidents.explain())

			if 'count' not in data and 'groupby' not in data:
				total = len(incidents)

				if 'count' not in data and 'page' in data and 'limit' in data and data['page'] > 0:
					incidents = incidents[(int(data['page']) - 1) * int(data['limit']) : (int(data['page']) - 1) * int(data['limit']) + int(data['limit'])]

				for item in incidents:
					incident_data.append({
						'incident_id': str(item.id) if 'id' in item else '',
						'category': item.category if 'category' in item else '',
						'subcategory': item.subcategory if 'subcategory' in item else '',
						'country': item.country if 'country' in item else '',
						'state': item.state if 'state' in item else '',
						'city': item.city if 'city' in item else '',
						'questions': item.questions if 'questions' in item else '',
						'rating': item.rating if 'rating' in item else '',
						'description': item.description if 'description' in item else '',
						'createdBy': item.user_name if 'user_name' in item else '',
						'image': str(item.image_id) if 'image_id' in item else None,
						'createdOn': round(time.mktime(item.date_added.timetuple())) if item.date_added else '' ,
					})
			else:
				try:
					total = incidents.count()
				except Exception as e:
					print('Exception', e)
					total = 0

		content = {
			'data': incident_data,
			'total': total,
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
