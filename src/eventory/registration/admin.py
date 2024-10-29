from django.contrib import admin
from .models import CustomUser, Interest, Event

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Interest)
admin.site.register(Event)
