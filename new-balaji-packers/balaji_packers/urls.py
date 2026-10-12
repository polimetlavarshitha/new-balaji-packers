"""
URL configuration for balaji_packers project.
"""
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "New Balaji Packers and Movers - Admin Portal"
admin.site.site_title = "Balaji Packers Portal"
admin.site.index_title = "Booking Orders & Logistics Management"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('packers.urls')),
]
