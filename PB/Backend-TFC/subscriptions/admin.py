from django.contrib import admin
from subscriptions.models import Plans, UserMemberships, UserPayHistory

# Register your models here.
admin.site.register(Plans)
admin.site.register(UserMemberships)
admin.site.register(UserPayHistory)