from django.contrib import admin

# Register your models here.
from .models import Login,Event
admin.site.register(Login)
admin.site.register(Event)

