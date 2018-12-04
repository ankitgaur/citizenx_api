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
	user_id = ObjectIdField(required=True)
	user_name = StringField(max_length=190, required=True)
	description = StringField(max_length=1000)
	date_added = DateTimeField(required=True)
	date_modified = DateTimeField(required=True)
	image_id = ObjectIdField(required=False)

	def __str__(self):
		return f'{self.id}'
