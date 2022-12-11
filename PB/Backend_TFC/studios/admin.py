from django.contrib import admin
from studios.models import Studio, Image, Amenities
# Register your models here.

class ImageInline(admin.TabularInline):
    model = Image
    fk_name = "studio"
    fields = ['image']
    extra = 0

class AmenitiesInline(admin.TabularInline):
    model = Amenities
    fk_name = "studio"
    fields = ['type', 'quantity']
    extra = 0

class StudioAdmin(admin.ModelAdmin):
    model = Studio
    fields = ['name', 'address', 'longitude', 'latitude', 'postal_code', 'phone_number']
    list_display = ['name', 'address', 'longitude', 'latitude', 'postal_code', 'phone_number']
    inlines = [ImageInline, AmenitiesInline]


admin.site.register(Studio, StudioAdmin)
admin.site.register(Image)
admin.site.register(Amenities)