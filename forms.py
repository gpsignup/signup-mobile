from django.forms import ModelForm
from signup.models import Event

class EventForm(ModelForm):
	class Meta:
		model = Event
