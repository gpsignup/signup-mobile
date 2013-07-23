from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from signup.models import Event, Slot, Person
from signup.forms import EventForm

def index(request):
	return render(request, 'index.html')

def create(request):
	if request.method == 'POST':
		new_event = EventForm(request.POST).save()		
		new_event.create_slots()
		return HttpResponseRedirect(reverse('signup.views.results', args=[new_event.id]))
	else:
		return render(request, 'create.html')

def results(request, event_id):	
	event = get_object_or_404(Event, id=event_id)	

	slot_list = event.slot_set.all().order_by('slot_start_time')
	date_dict = {}
	slots_by_time = {}
	time_str_list = []
	
	# Make data for timetable template
	for slot in slot_list:
		date_dict[slot.slot_day] = 1
		time_str = ''.join([str(slot.slot_start_time)[:-3],' - ',str(slot.slot_end_time)[:-3]])
		if not time_str in time_str_list:
			slots_by_time[time_str] = []
			time_str_list.append(time_str)			
		slots_by_time[time_str].append(slot)

	return render(request, 'results_by_dates.html', {'date_dict': date_dict,
										 			'slots_by_time': slots_by_time,
										 			'event': event})
	
def view(request, event_id):
	if request.method == 'POST':
		event = get_object_or_404(Event, id=event_id)
		slot_list = event.slot_set.all()
		sign_up_slot_list = request.POST.getlist('signed_up_slots')
		person_name = request.POST['person_name']
		email = request.POST['email']

		# Update or Create person
		(person,created) = Person.objects.get_or_create(person_name=person_name,
														email=email)
				
		for slot_id in sign_up_slot_list:			
			slot = Slot.objects.get(id=slot_id)
			slot.people.add(person)

		return HttpResponseRedirect(reverse('signup.views.thanks'))
	else:
		event = get_object_or_404(Event, id=event_id)
		slot_list = event.slot_set.all().order_by('slot_start_time')
		date_dict = {}
		slots_by_time = {}
		time_str_list = []
		
		# Make data for timetable template
		for slot in slot_list:
			date_dict[slot.slot_day] = 1
			time_str = ''.join([str(slot.slot_start_time)[:-3],' - ',str(slot.slot_end_time)[:-3]])
			if not time_str in time_str_list:
				slots_by_time[time_str] = []
				time_str_list.append(time_str)			
			slots_by_time[time_str].append(slot)

		return render(request, 'view_by_dates.html', {'date_dict': date_dict,
											 		  'slots_by_time': slots_by_time,
											 		  'event': event})

def manage(request):
	if request.method == 'POST':
		print request.POST['is_mobile']=='False'
		return HttpResponseRedirect(reverse('signup.views.results', 
											args=[request.POST['event_id']]))
	else:
		event_list = Event.objects.all().order_by('event_start_day', 'event_start_time')	
		return render(request, 'manage.html', {'event_list': event_list})

def signup(request):
	if request.method == 'POST':
		return HttpResponseRedirect(reverse('signup.views.view', 
											args=[request.POST['event_id']]))
	else:
		event_list = Event.objects.all().order_by('event_start_day', 'event_start_time')	
		return render(request, 'signup.html', {'event_list': event_list})

def thanks(request):	
	return render(request, 'thanks.html')
