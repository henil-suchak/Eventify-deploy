from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.utils import timezone
from django.utils.timezone import now
from datetime import datetime
from io import BytesIO
import qrcode
from .models import Event, Attendee, AttendeeRequest
from .forms import EventForm
from eventify.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

# ---------------------------------------------------------------------------------------------------------------------------
#3 home page
def home(request):
    return render(request, 'event/home.html')

# ---------------------------------------------------------------------------------------------------------------------------
#4 event list page
@login_required
def event_list(request):
    current_time = timezone.now()
    upcoming_events = Event.objects.filter(date_time__gt=current_time).order_by('date_time')
    
    return render(request, 'event/event_list.html', {'events': upcoming_events, 'current_time': current_time})

# ---------------------------------------------------------------------------------------------------------------------------
#5 past events
@login_required
def past_events(request):
    past_events = Event.objects.filter(date_time__lt=timezone.now()).order_by('-date_time') 
    return render(request, 'event/past_events.html', {'events': past_events})

# ---------------------------------------------------------------------------------------------------------------------------
#6 create event page
@login_required
def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user  # Assign the event organizer
            event.save()
            return redirect('event:event_list')
    else:
        form = EventForm()
    
    return render(request, 'event/create_event.html', {'form': form})

# ---------------------------------------------------------------------------------------------------------------------------
#7 event details page
@login_required
def event_details(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'event/event_details.html', {'event': event})

# ---------------------------------------------------------------------------------------------------------------------------
#8.1 Register for Event
def register_user_page(request, event_id):
    """ Renders the registration page where users enter their details """
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event/register_user.html', {'event': event})

#8.2 Register for Event Submit
def register_user(request, event_id):
    """ Handles form submission for event registration """
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_no = request.POST.get("phone")

        attendee, created = Attendee.objects.get_or_create(
            email=email, defaults={"name": name, "phone_no": phone_no}
        )

        if AttendeeRequest.objects.filter(event=event, attendee=attendee).exists():
            messages.warning(request, "You have already requested to join this event.")
        else:
            AttendeeRequest.objects.create(event=event, attendee=attendee)
            messages.success(request, "Your request has been sent to the organizer.")
        return redirect('event:event_details', event_id=event.id)
    return redirect('event:register_user_page', event_id=event.id)

#8.3 Register for Event
@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Ensure user is not already registered
    if request.user not in event.attendees.all():
        event.attendees.add(request.user)
        messages.success(request, "Successfully registered for the event.")
    
    return redirect('event:event_details', event_id=event.id)

# ---------------------------------------------------------------------------------------------------------------------------
#9 edit event page
@login_required
def edit_event(request, event_id):  # Use title instead of event_id
    event = get_object_or_404(Event, id=event_id,organizer=request.user)  # Get event by title
    
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event:event_details', event_id)  # Redirect after saving
    else:
        form = EventForm(instance=event)

    return render(request, 'event/edit_event.html', {'form': form, 'event': event})

# ---------------------------------------------------------------------------------------------------------------------------
#10.1 manage attendee event page
@login_required
def manage_attendee_requests(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user != event.organizer:
        messages.error(request, "You are not authorized to manage this event.")
        return redirect('event:event_list')

    pending_requests = AttendeeRequest.objects.filter(event=event, is_approved=False)

    if request.method == "POST":
        attendee_id = request.POST.get("attendee_id")
        action = request.POST.get("action")
        attendee_request = get_object_or_404(AttendeeRequest, event=event, attendee_id=attendee_id)

        if action == "approve":
            attendee_request.is_approved = True
            attendee_request.save()
            event.attendees.add(attendee_request.attendee)  # Add to approved attendees
            # messages.success(request, f"{attendee_request.attendee.name} has been approved.")
        elif action == "reject":
            attendee_request.delete()
            # messages.info(request, f"{attendee_request.attendee.name} has been rejected.")

        return redirect('event:manage_event', event_id=event.id)

    return render(request, 'event/manage_event.html', {'event': event, 'pending_requests': pending_requests})

#10.2 approve attendee request page
@login_required
def approve_attendee(request, event_id, attendee_id):
    event = get_object_or_404(Event, id=event_id)
    attendee = get_object_or_404(Attendee, id=attendee_id)
    attendee_request = get_object_or_404(AttendeeRequest, event=event, attendee=attendee)

    if request.user == event.organizer:
        attendee_request.is_approved = True
        attendee_request.save()
        event.attendees.add(attendee)  # Add attendee to the confirmed list

        # Generate unique QR Code
        qr_data = f"Event: {event.title}\nAttendee: {attendee.name}\nEmail: {attendee.email}"
        qr = qrcode.make(qr_data)

        # Save QR code to memory
        qr_io = BytesIO()
        qr.save(qr_io, format="PNG")
        qr_io.seek(0)

        # Create email with QR code attachment
        subject = f"Event Confirmation: {event.title}"
        message = f"""
        Dear {attendee.name},

        Congratulations! You have been approved to attend the event "{event.title}".

        Event Details:
        - Organizer: {event.organizer.name}
        - Description: {event.description}
        - Location: {event.location}
        - Date & Time: {event.date_time.strftime('%Y-%m-%d %H:%M')}
        
        Please find your unique QR Code attached. Show this at the event entrance.

        Best Regards,  
        Eventify Team
        """

        sender_email = "123eventify@gmail.com"
        recipient_email = [attendee.email]

        email = EmailMessage(subject, message, sender_email, recipient_email)
        email.attach(f"QR_{attendee.name}.png", qr_io.getvalue(), "image/png")

        try:
            email.send()
            messages.success(request, f"{attendee.name} has been approved, and an email has been sent!")
        except Exception as e:
            messages.error(request, f"Approval successful, but email failed: {str(e)}")

    return redirect('event:manage_event', event_id=event.id)

#10.3 reject attendee request page
@login_required
def reject_attendee(request, event_id, attendee_id):
    event = get_object_or_404(Event, id=event_id)
    attendee = get_object_or_404(Attendee, id=attendee_id)
    attendee_request = get_object_or_404(AttendeeRequest, event=event, attendee=attendee)

    if request.user == event.organizer:
        attendee_request.delete()  # Remove request
        # messages.info(request, f"{attendee.name} has been rejected.")

    return redirect('event:manage_event', event_id=event_id)

#10.4 remove attendee from event page
def remove_attendee(request, event_id, attendee_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user != event.organizer:
        messages.error(request, "You do not have permission to remove attendees.")
        return redirect('event:manage_event', event_id=event.id)

    attendee = get_object_or_404(Attendee, id=attendee_id)
    attendee_request = get_object_or_404(AttendeeRequest, event=event, attendee=attendee)

    # Move back to pending state instead of deleting
    attendee_request.is_approved = False
    attendee_request.save()

    event.attendees.remove(attendee)  # Remove attendee from confirmed list

    # messages.success(request, f"{attendee.name} has been moved back to pending requests.")
    return redirect('event:manage_event', event_id=event.id)

# ---------------------------------------------------------------------------------------------------------------------------
#11, 12 profile page
@login_required
def profile(request):
    # Get upcoming events organized by the currently logged-in user
    upcoming_events = Event.objects.filter(organizer=request.user, date_time__gte=now()).select_related('organizer')

    return render(request, 'event/profile.html', {'upcoming_events': upcoming_events})

# ---------------------------------------------------------------------------------------------------------------------------
#13 profile past events
@login_required
def profile_past(request):
    # Get past events organized by the currently logged-in user
    past_events = Event.objects.filter(organizer=request.user, date_time__lt=datetime.now()).select_related('organizer')
    
    return render(request, 'event/profile_past.html', {'user': request.user, 'past_events': past_events})

# ---------------------------------------------------------------------------------------------------------------------------
#15 past event details page
def past_event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Ensure it's a past event (assuming `event.date_time` is a DateTimeField)
    if event.date_time >= timezone.now():
        return redirect("event:event_details", event_id=event.id)

    return render(request, "event/past_event_details.html", {"event": event})

# ---------------------------------------------------------------------------------------------------------------------------
#16 delete event page
@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, organizer=request.user)
    event.delete()
    return redirect('event:event_list')

# ---------------------------------------------------------------------------------------------------------------------------
#17 send email to attendees page
@login_required
def send_email_to_attendees(request, event_id):
    """Send a reminder email to all attendees of the event."""
    event = get_object_or_404(Event, id=event_id)
    attendees = event.attendees.all()

    if not attendees:
        messages.error(request, "No attendees to send emails to.")
        return redirect('event:manage_event', event_id=event.id)

    recipients = [attendee.email for attendee in attendees if attendee.email]

    if not recipients:
        messages.error(request, "No valid email addresses found.")
        return redirect('event:manage_event', event_id=event.id)

    subject = f"📅 Reminder: {event.title}"
    message = f"""
    Dear Attendee,

    This is a reminder about the upcoming event: {event.title}.

    📌 Event Details:
    - Description: {event.description}
    - Location: {event.location}
    - Date & Time: {event.date_time.strftime('%Y-%m-%d %H:%M')}

    Looking forward to seeing you there!

    Best Regards,  
    {request.user.name if request.user.name else request.user.email}
    """

    try:
        send_mail(subject, message, request.user.email, recipients)
        messages.success(request, f"Emails sent successfully for '{event.title}'!")
    except Exception as e:
        messages.error(request, f"Failed to send emails: {str(e)}")

    return redirect('event:manage_event', event_id=event.id)
