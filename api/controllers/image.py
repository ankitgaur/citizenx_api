from django.http import HttpResponse
from django.views import View
from django.conf import settings
from django.core.files.storage import FileSystemStorage

import json, datetime, time, re, mimetypes

from ..models.image import Image as Model
from ..models.incident import Incident

class Image(View):
	image = Model()

	def get(self, request, *args, **kwargs):
		error = ''
		status = 200
		mimetype = 'application/json'
		data = ''
		error = ''

		if 'id' not in kwargs:
			error = 'Image id is required'
			status = 400

		if not error:
			image = Model.objects(id = kwargs['id'])

			if image.count() <= 0:
				status = 404
				error = 'No record found'
			else:
				item = image.first()

				with open(settings.BASE_DIR + item.image, 'rb+') as f:
					data = f.read()

				mimetype = mimetypes.guess_type(settings.BASE_DIR + item.image)
				mimetype = mimetype[0]

		if not data:
			data = json.dumps({
				'data': {},
				'status': False if error else True,
				'error': error
			})

		httpresponse = HttpResponse(data, content_type = mimetype)
		httpresponse.status_code = status

		return httpresponse

	def put(self, request, *args, **kwargs):
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
		status = 200

		try:
			data = request.POST

			if 'id' not in kwargs:
				error = 'Incident id is required'
				status = 400
			#if 'incident_id' not in data or not data['incident_id']:
			#	error = 'Incident ID is required'
			#	status = 400
			else:
				#incident = Incident.objects(id = data['incident_id'])
				incident = Incident.objects(id = kwargs['id'])

				if incident.count() <= 0:
					error = 'Invalid Incident ID'
					status = 404
				else:
					incident = incident.first()

			if 'file' not in request.FILES and not request.FILES['file']:
				error = 'File is required'
				status = 400
			else:
				if ['image/png', 'image/jpeg', 'image/svg+xml'].count(request.FILES['file'].content_type) == 0:
					error = 'Invalid File Type'
					status = 400
				if request.FILES['file'].size > (5 * 1024 * 1024):
					error = 'File Size should be less than 5MB'
					status = 400

			file = self.upload(request)

			if not file:
				error = 'File not uploaded'
				status = 400

			if not error:
				self.image = Model()
				self.image.image = file
				self.image.incident_id = incident['id']
				self.image.incident_name = incident['category']
				self.image.user_id = request.session['user_id']
				self.image.user_name = request.session['user_name']
				self.image.date_added = datetime.datetime.now()
				self.image.date_modified = datetime.datetime.now()

				self.image.save()
		except Exception as e:
			error = str(e)
			status = 400

		content = {
			'data': None,
			'status': False if error else True,
			'error': error,
			'id': str(self.image)
		}

		incident.image_id = content['id']
		incident.save()

		print(incident)
		print(content)
		print(content['error'])

		return self.response(content, status_code = status)

	def delete(self, request, *args, **kwargs):
		error = ''
		status = 200

		if 'id' not in kwargs:
			error = 'Image id is required'
			status = 400

		if not error:
			Model.objects(id = kwargs['id']).delete()

		content = {
			'data': None,
			'status': False if error else True,
			'error': error
		}

		return self.response(content, status_code = status)

	def upload(self, request):
		if request.method == 'POST' and request.FILES['file']:
			file = request.FILES['file']
			fs = FileSystemStorage()
			filename = fs.save(re.sub(r'\s+', '-', file.name.strip()), file)
			return fs.url(filename)

	def response(self, data, status_code = 200):
		httpresponse = HttpResponse(json.dumps(data), content_type = 'application/json')
		httpresponse.status_code = status_code

		return httpresponse
