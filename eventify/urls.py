from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from event.views import event_list  # Import your event list view
from django.conf import settings
from django.conf.urls.static import static
import user1

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='user1/login.html'), name='login'),  # Login Page as Default

    path('event/', include('event.urls')),  # Include app URLs


    path('user1/',include('user1.urls')),

    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
