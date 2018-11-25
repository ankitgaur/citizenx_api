from mongoengine import *
# Create your models here.

class Poll(Document):
	title = StringField(max_length=190, required=True)
	options = ListField(DictField())
	date_added = DateTimeField(required=True)
	date_modified = DateTimeField(required=True)

	def __str__(self):
		return f'{self.id}'
