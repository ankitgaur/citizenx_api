from django.http import HttpResponse
from django.views import View
from django.conf import settings

import json, datetime, time

from ..models.sentiment import Sentiment as Model

class SentimentFilter(View):
	sentiment = Model()

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

		sentiment_data = []
		daterange = {}

		if not error:
			filter = {}

			data = json.loads(request.body)

			print('Applying Filters on data ', data)

			if 'incident_id' in data:
				filter['incident_id'] = data['incident_id']

			if 'incident_name' in data:
				filter['incident_name__iexact'] = data['incident_name']

			if 'date_range' in data:
				explode = data['date_range'].split('-')

				if len(explode) > 1:
					print('Filtering date range', datetime.datetime.fromtimestamp(round(int(explode[0]) / 1000)), datetime.datetime.fromtimestamp(round(int(explode[1]) / 1000)))

					#filter['date_added'] = {
					daterange = {
						'$lte': datetime.datetime.fromtimestamp(round(int(explode[0]) / 1000)),
						'$gte': datetime.datetime.fromtimestamp(round(int(explode[1]) / 1000))
					}

			print('Filtering sentiments', filter)

			if 'sort' in data:
				if 'order' in data and data['order'] == 'desc':
					data['sort'] = '-' + data['sort']

				sentiments = Model.objects(**filter).order_by(data['sort'])
			else:
				sentiments = Model.objects(**filter)

			if 'distinct' in data:
				sentiments = sentiments.distinct(data['distinct'])

			if 'groupby' in data:
				if data['groupby'] == 'day':
					groupbyid = {
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
								'date_added': daterange
							}
						},
						{
							'$group': {
								'_id': groupbyid,
								'total': { '$sum': 1 }
							}
						},
						{
							'$sort': { 'total': -1 }
						}
					]
				elif data['groupby'] == 'month':
					groupbyid = {
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
								'date_added': daterange
							}
						},
						{
							'$group': {
								'_id': groupbyid,
								'total': { '$sum': 1 }
							}
						},
						{
							'$sort': { 'total': -1 }
						}
					]
				else:
					groupbyid = '$' + data['groupby']

					pipeline = [
						{
							'$group': {
								'_id': groupbyid,
								'total': { '$sum': 1 }
							}
						},
						{
							'$sort': { 'total': -1 }
						}
					]

				print('Group By', pipeline)

				sentiments = sentiments.aggregate(*pipeline)

				for item in sentiments:
					sentiment_data.append({
						data['groupby']: item['_id'] if '_id' in item else '',
						'total': item['total'] if 'total' in item else 0
					})

			#print('Mongo Query', sentiments.explain())

			if 'count' not in data and 'groupby' not in data:
				total = len(sentiments)

				if 'count' not in data and 'page' in data and 'limit' in data and data['page'] > 0:
					sentiments = sentiments[(int(data['page']) - 1) * int(data['limit']) : (int(data['page']) - 1) * int(data['limit']) + int(data['limit'])]

				for item in sentiments:
					sentiment_data.append({
						'sentiment_id': str(item.id),
						'sentiment': item.sentiment,
						'incident_id': str(item.incident_id),
						'incident_name': item.incident_name,
						'user_id': str(item.user_id),
						'createdBy': item.user_name,
						'createdOn': round(time.mktime(item.date_added.timetuple())),
					})
			else:
				try:
					total = sentiments.count()
				except Exception as e:
					print('Exception', e)
					total = 0

		content = {
			'data': sentiment_data,
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
