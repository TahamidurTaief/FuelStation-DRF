from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Include the urls.py from your 'api' app
]



# Developed by
# Tahamidur Taief
# full stack Python Developer.