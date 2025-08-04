# from django.db import models
# from django.utils import timezone
# # Create your models here.

# class Login(models.Model):
#     email = models.EmailField(max_length=100, null=True)
#     password = models.CharField(max_length=100, null=True)
#     userType = models.CharField(max_length=100, null=True)


# class Event(models.Model):
#     title = models.CharField(max_length=255)
#     image= models.ImageField(max_length=100, null=True)
#     description = models.TextField()
#     datetime = models.DateTimeField()
#     venue = models.CharField(max_length=255)
#     capacity = models.IntegerField()
#     regdead = models.DateTimeField()

#     def __str__(self):
#         return self.title
# class UserReg(models.Model):
#     usrid = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)
#     name = models.CharField(max_length=100, null=True)
#     email = models.EmailField(max_length=100, null=True)
#     password = models.CharField(max_length=100, null=True)
#     phone = models.CharField(max_length=100, null=True)

#     gender = models.CharField(max_length=100, null=True)
#     address = models.CharField(max_length=100, null=True)
    
#     def __str__(self):
#         return self.name
    
# from django.db import models
# from django.utils import timezone
# from django.db import models
# from django.utils import timezone
# from .models import Event  # assuming Event is in the same app
# from django.contrib.auth.models import User

# class Booking(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
#     booking_date = models.DateTimeField(default=timezone.now)
#     is_cancelled = models.BooleanField(default=False)
#     seats_booked = models.PositiveIntegerField(default=1)


#     class Meta:
#         unique_together = ('email', 'event')  # Prevent duplicate bookings

#     def __str__(self):
#         return f"{self.name} - {self.event.title}"

#     def status(self):
#         if self.is_cancelled:
#             return "Cancelled"
#         elif timezone.now() > self.event.datetime:
#             return "Past"
#         return "Confirmed"
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Login(models.Model):
    email = models.EmailField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    userType = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.email or "Login"


class Event(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    description = models.TextField()
    datetime = models.DateTimeField()
    venue = models.CharField(max_length=255)
    capacity = models.IntegerField()
    regdead = models.DateTimeField()

    def __str__(self):
        return self.title


class UserReg(models.Model):
    usrid = models.ForeignKey(Login, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(default=timezone.now)
    is_cancelled = models.BooleanField(default=False)
    seats_booked = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('email', 'event')

    def __str__(self):
        return f"{self.name} - {self.event.title}"

    def status(self):
        if self.is_cancelled:
            return "Cancelled"
        elif timezone.now() > self.event.datetime:
            return "Past"
        return "Confirmed"
