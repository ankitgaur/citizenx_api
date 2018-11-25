from mongoengine import *
# Create your models here.

class PollService(Document):
	poll_title = StringField(max_length=190, required=True)
	poll_option = StringField(max_length=1, required=True)
	poll_option_text = StringField(max_length=190, required=True)
	date_added = DateTimeField(required=True)
	date_modified = DateTimeField(required=True)

	def __str__(self):
		return f'{self.id}'
