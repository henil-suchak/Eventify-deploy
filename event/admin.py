from django.contrib import admin
from .models import Event, Attendee, AttendeeRequest

# Register Attendee model
admin.site.register(Attendee) 

# Custom admin class for Event
class EventAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "attendees":
            if request.resolver_match and request.resolver_match.kwargs.get("object_id"):
                event_id = request.resolver_match.kwargs["object_id"]
                kwargs["queryset"] = Attendee.objects.filter(events__id=event_id) 
            else:
                kwargs["queryset"] = Attendee.objects.none()
        return super().formfield_for_manytomany(db_field, request, **kwargs)

# Register Event model with custom admin class
admin.site.register(Event, EventAdmin)

# Custom admin class for AttendeeRequest
@admin.register(AttendeeRequest)
class AttendeeRequestAdmin(admin.ModelAdmin):
    list_display = ("attendee", "event", "requested_at", "is_approved", "is_attending")  # Display columns
    list_filter = ("is_approved", "is_attending")  # Add filters for status
    search_fields = ("attendee__name", "event__title")  # Enable search