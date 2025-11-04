from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

# from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # ✅ include the app’s URLs
    path('', include('users.urls')),  # ✅ include the users app’s URLs
    
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root = settings.MEDIA_ROOT)
    
