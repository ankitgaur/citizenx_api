from mongoengine import *
# Create your models here.

class Image(Document):
	image = StringField(max_length=255, required=True)
	incident_id = ObjectIdField(required=False)
	incident_name = StringField(max_length=190, required=False)
	user_id = ObjectIdField(required=True)
	user_name = StringField(max_length=190, required=True)
	date_added = DateTimeField(required=True)
	date_modified = DateTimeField(required=True)

	def __str__(self):
		return f'{self.id}'
