from django.contrib import admin
from .models import Listing
# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )


admin.site.register(Listing, ListingAdmin)