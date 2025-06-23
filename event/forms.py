from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import Event

#-----------------------------------------------------------------------------------------------------------------------------------
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'date_time', 'image', 'max_attendees']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg shadow-sm text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-orange-500'}),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg shadow-sm text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-orange-500',
                'rows': 8,  # Increased height
            }),
            'location': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg shadow-sm text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-orange-500'}),
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full px-4 py-2 border rounded-lg shadow-sm text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-orange-500'}),
            'max_attendees': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg shadow-sm text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-orange-500'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg shadow-sm text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-orange-500'}),
        }

    def clean_date_time(self):
        event_date = self.cleaned_data.get('date_time')
        min_time = timezone.now() + timedelta(hours=5)

        if event_date and event_date < min_time:
            raise forms.ValidationError("Event must be scheduled at least 5 hours from now.")

        return event_date
    
#-----------------------------------------------------------------------------------------------------------------------------------
