from mongoengine import *
# Create your models here.

class State(Document):
	name = StringField(max_length=255, required=True)

	def __str__(self):
		return f'{self.id}'
