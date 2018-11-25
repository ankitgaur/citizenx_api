from mongoengine import *
# Create your models here.

class Sentiment(Document):
	sentiment = IntField(min_value=1, max_value=5)
	incident_id = ObjectIdField(required=True)
	incident_name = StringField(max_length=190, required=True)
	user_id = ObjectIdField(required=True)
	user_name = StringField(max_length=190, required=True)
	date_added = DateTimeField(required=True)
	date_modified = DateTimeField(required=True)

	def __str__(self):
		return f'{self.id}'
