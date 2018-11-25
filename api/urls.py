from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views
from .controllers.incidents import Incident
from .controllers.incident_filter import IncidentFilter
from .controllers.user import User
from .controllers.state import State
from .controllers.sentiment import Sentiment
from .controllers.comment import Comment
from .controllers.image import Image

urlpatterns = [
	path('getincidents/', csrf_exempt(IncidentFilter.as_view())),
	path('incident/<id>/', csrf_exempt(Incident.as_view())),
	path('user/user-info/', csrf_exempt(User.as_view())),
	path('user/login/', csrf_exempt(User.as_view())),
	path('user/register/', csrf_exempt(User.as_view())),
	path('states/', csrf_exempt(State.as_view())),
	path('incident/', csrf_exempt(Incident.as_view())),
	path('sentiment/<id>/', csrf_exempt(Sentiment.as_view())),
	path('sentiment/', csrf_exempt(Sentiment.as_view())),
	path('comment/<id>/', csrf_exempt(Comment.as_view())),
	path('comment/', csrf_exempt(Comment.as_view())),
	path('image/<id>/', csrf_exempt(Image.as_view())),
	path('image/', csrf_exempt(Image.as_view())),
	#path('poll/<id>/', Poll.as_view(), name='get'),
	#path('poll/', csrf_exempt(Poll.as_view())),
	#path('user-poll/<id>/', User.as_view(), name='get'),
	#path('user-poll/', csrf_exempt(User.as_view())),
]
