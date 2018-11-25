from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

import json, datetime, uuid

def index(request):
	content = {
		'test': 'test'
	}

	return response(content, status_code = 200)

def response(data, status_code = 200):
	httpresponse = HttpResponse(json.dumps(data), content_type = 'application/json')
	httpresponse.status_code = status_code
	return httpresponse
