from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),        # Admin panel URL
    path('api/', include('panel.urls')),    # Include the panel app's URLs under 'api/'
]
