from django.db import models
from django.contrib import admin
import datetime
#------------------------------------------------------------------------------- 
class Event(models.Model):
	event_name = models.CharField(max_length=100)
	location = models.CharField(max_length=100)
	event_start_day = models.DateField('event_start_day')
	event_end_day = models.DateField('event_end_day')
	event_start_time = models.TimeField('event_start_time')
	event_end_time = models.TimeField('event_end_time')
	slot_duration = models.PositiveIntegerField()
	slot_capacity = models.PositiveIntegerField()
	
	def create_slots(self):		
		current_day = self.event_start_day
		current_time = self.event_start_time
		while current_day <= self.event_end_day:
			while current_time < self.event_end_time:
				interval = datetime.timedelta(minutes=int(self.slot_duration))
				interval_end = (datetime.datetime.combine(datetime.date(1,1,1),current_time) + interval).time()
				self.slot_set.create(slot_day=current_day,
									 slot_start_time=current_time,
									 slot_end_time=interval_end)
				current_time = interval_end				
			current_time = self.event_start_time
			current_day += datetime.timedelta(days=1)

	def __unicode__(self):
		return unicode(self.event_name)
#-------------------------------------------------------------------------------
class Person(models.Model):
	person_name = models.CharField(max_length=100)
	email = models.EmailField()

	def __unicode__(self):
		return unicode(self.person_name)
#-------------------------------------------------------------------------------
class Slot(models.Model):
	slot_day = models.DateField('slot_day')
	slot_start_time = models.TimeField('slot_start_time')
	slot_end_time = models.TimeField('slot_end_time')
	event = models.ForeignKey(Event)
	people = models.ManyToManyField(Person, blank=True, null=True)

	def __unicode__(self):
		return unicode(''.join([str(self.event),str(self.slot_day),str(self.slot_start_time),str(self.slot_end_time)]))

	def is_full(self):
		capacity = self.event.slot_capacity
		current_size = len(self.people.all())
		return current_size >= capacity
#-------------------------------------------------------------------------------
admin.site.register(Event)
admin.site.register(Slot)
admin.site.register(Person)