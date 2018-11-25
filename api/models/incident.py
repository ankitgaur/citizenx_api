from mongoengine import *
# Create your models here.

class Incident(Document):
	category = StringField(max_length=190, required=True)
	subcategory = StringField(max_length=190, required=True)
	country = StringField(max_length=190, required=True)
	state = StringField(max_length=190, required=True)
	city = StringField(max_length=190, required=True)
	questions = ListField(DictField())
	rating = StringField(max_length=1)
	description = StringField(max_length=1000)
	date_added = DateTimeField(required=True)
	date_modified = DateTimeField(required=True)

	def __str__(self):
		return f'{self.id}'
