from django.contrib import admin
from .models import Listing
# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    pass


admin.site.register(Listing, ListingAdmin)