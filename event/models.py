from django.db import models
from user1.models import CustomUser

#-----------------------------------------------------------------------------------------------------------------------------------
class Attendee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_no = models.CharField(max_length=15, null=True, blank=True) 

    def __str__(self):
        return self.name

#-----------------------------------------------------------------------------------------------------------------------------------
class Event(models.Model):
    title = models.CharField(max_length=200)  
    description = models.TextField()
    location = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    attendees = models.ManyToManyField(Attendee, related_name='events', blank=True) 
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    max_attendees = models.PositiveIntegerField(default=100)
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="organized_events", null=True, blank=True)

    def __str__(self):
        return self.title

#-----------------------------------------------------------------------------------------------------------------------------------
class AttendeeRequest(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="attendee_requests")
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # Default is pending approval
    is_attending = models.BooleanField(default=True)  # Track if attendee is still attending

    def __str__(self):
        status = "Going" if self.is_attending else "Not Going"
        return f"{self.attendee.name} requested for {self.event.title} - {status}"
