from django.contrib import admin
from .models import Login, Event, UserReg, Booking

# admin.site.register(Login)
# admin.site.register(Event)
# admin.site.register(UserReg)
# admin.site.register(Booking)
from django.contrib import admin
from .models import Login, Event, UserReg, Booking


@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'userType')
    search_fields = ('email', 'userType')
    list_filter = ('userType',)


@admin.register(UserReg)
class UserRegAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'gender')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('gender',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'venue', 'datetime', 'regdead', 'capacity')
    search_fields = ('title', 'venue')
    list_filter = ('venue', 'datetime')
    ordering = ('-datetime',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'event', 'booking_date', 'seats_booked', 'status')
    search_fields = ('name', 'email', 'event__title')
    list_filter = ('event', 'is_cancelled')
    date_hierarchy = 'booking_date'
    ordering = ('-booking_date',)
