from django.urls import path
from .views import main_view

from .views import home_view, main_view, list_view, listing_view
urlpatterns = [
    path('', main_view, name='main'),  # ✅ root of app
    path('home/', home_view, name='home'),  # ✅ home page
    path('list/', list_view, name='list'),  # ✅ list page
    path('listing/<str:id>/', listing_view, name='listing'),  # ✅ listing page
]
