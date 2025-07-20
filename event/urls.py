from django.urls import path, include
from . import views
from django.urls import path
from .views import send_email_to_attendees

# localhost:8000/event/
app_name = "event"  # Namespace for the app

urlpatterns = [
    path('home/', views.home, name='home'), #3 Home page

    path('', views.event_list, name='event_list'), #4 Upcoming events

    path('events/past/', views.past_events, name='past_events'), #5 past events

    path('create_event/', views.create_event, name='create_event'), #6 create event

    path('<int:event_id>/', views.event_details, name="event_details"), #7 Event details

    path('event/<int:event_id>/register/', views.register_user_page, name='register_user_page'), #8.1 register for event page
    path('event/<int:event_id>/register/submit/', views.register_user, name='register_user'), #8.2 register for event submit

    path('<int:event_id>/edit_event/', views.edit_event, name='edit_event'), #9 edit event

    path('event/<int:event_id>/manage/', views.manage_attendee_requests, name='manage_event'), #10.1 Manage event attendee requests
    path('approve-attendee/<int:event_id>/<int:attendee_id>/', views.approve_attendee, name='approve_attendee'), #10.2, 17 Approve attendee request
    path('reject-attendee/<int:event_id>/<int:attendee_id>/', views.reject_attendee, name='reject_attendee'), #10.3 Reject attendee request
    path('event/<int:event_id>/remove-attendee/<int:attendee_id>/', views.remove_attendee, name='remove_attendee'), #10.4 Remove attendee from event

    path('profile/', views.profile, name='profile'), #11, 12 Profile page

    path('profile/past/', views.profile_past, name='profile_past'), #13 Profile past events

    path("past-event/<int:event_id>/", views.past_event_details, name="past_event_details"), #15 past event details

    path('<int:event_id>/delete_event/', views.delete_event, name='delete_event'), #16 Delete Event

    path('event/<int:event_id>/send-email/', send_email_to_attendees, name='send_email_to_attendees'), #18 Send email to all attendees

    path("scan_qr/", views.scan_qr_code, name="scan_qr"), #20
    
    path('payments/', include('payments.urls')), # Include your payment app's URLs

]