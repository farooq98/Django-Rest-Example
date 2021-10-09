from django.contrib import admin
from django.urls import path, include
from .custom_admin import custom_admin_site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('custom-admin/', custom_admin_site.urls),
    path('api/', include("posts.urls")),
    path('api/register/', include("user_registration.urls")),
    path('api/core/', include("myapp.urls")),
    path('api/games/', include("games.urls")),
    path('chat/', include('chat.urls')),
]