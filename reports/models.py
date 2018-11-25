from mongoengine import *
# Create your models here.

class User(Document):
	name = StringField(max_length=190, required=True)
	email = StringField(max_length=190, required=True)
	username = StringField(max_length=120, required=True)
	password = StringField(max_length=255, required=True)
	date_added = DateTimeField(required=True)
	date_modified = DateTimeField(required=True)
