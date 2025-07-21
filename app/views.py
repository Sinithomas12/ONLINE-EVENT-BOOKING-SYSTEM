from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Login,Event,UserReg# Adjust the import based on your app
from django.utils import timezone
from app.models import UserReg

def index(request):
    return render(request,'index.html')

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages

def login(request):
    msg = request.GET.get('msg', '')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            data = Login.objects.get(email=email, password=password)

            if data.userType == "admin":
                msg = "Welcome to Admin Page"
                return render(request,'admin.html')

            elif data.userType == "user":
                try:
                  
                     return redirect('userviewevent')
                except ObjectDoesNotExist:
                    msg = "User does not exist"

        except ObjectDoesNotExist:
            msg = "Invalid username or password provided"

    return render(request, 'login.html', {'msg': msg})
from django.utils import timezone
from django.shortcuts import render
from .models import Event

def addevent(request):
    msg = ""

    if request.method == "POST":
        title = request.POST.get("title")

        if Event.objects.filter(title=title).exists():
            msg = "Event with this title already exists."
        else:
            image = request.FILES.get("image")
            description = request.POST.get("description")
            datetime = request.POST.get("datetime")
            venue = request.POST.get("venue")
            capacity = request.POST.get("capacity")
            regdead = request.POST.get("regdead")

            Event.objects.create(
                image=image,
                title=title,
                description=description,
                venue=venue,
                datetime=datetime,
                capacity=capacity,
                regdead=regdead
            )
            msg = "Event added successfully."

    events = Event.objects.filter(datetime__gte=timezone.now())
    return render(request, 'adminadd.html', {"msg": msg, "events": events})

def userreg(request):
    msg = ""
    msg = request.GET.get('msg')
    if request.POST:
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        address = request.POST.get("address")
        gender = request.POST.get("gender")

        if UserReg.objects.filter(email=email).exists() or Login.objects.filter(email=email).exists():
            msg = "Email Already Registered"
        else:
            abc = Login.objects.create(
                email=email, password=password, userType='user')
            abc.save()
            reg = UserReg.objects.create(name=name, email=email, address=address,
                                         phone=phone, password=password, usrid=abc, gender=gender)
            reg.save()
            msg = "Registration Successful"
    return render(request, 'userreg.html', {"msg": msg})
def userviewevent(request):
    msg = request.GET.get('msg')
    events = Event.objects.all()
    bookings = Booking.objects.all()  # get all bookings
    
    return render(request, 'userhome.html', {
        "events": events,
        "bookings": bookings,
        "msg": msg
    })

from django.contrib import messages
from app.models import Event, Booking
from django.utils import timezone
def userviewevent(request):
    msg = request.GET.get('msg')

    # Only show events where registration deadline is still open and event date is in the future
    events = Event.objects.filter(regdead__gte=timezone.now(), datetime__gte=timezone.now())

    user_bookings = []
    if request.user.is_authenticated:
        user_bookings = Booking.objects.filter(user=request.user).values_list('event_id', flat=True)

    return render(request, 'userhome.html', {
        "events": events,
        "user_bookings": user_bookings,
        "msg": msg
    })

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils import timezone

def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")

        # Validation checks
        if timezone.now() > event.regdead:
            messages.error(request, "Registration deadline has passed.")
            return redirect('userviewevent')

        if Booking.objects.filter(event=event, email=email).exists():
            messages.warning(request, "You have already booked this event.")
            return redirect('userviewevent')

        if event.bookings.count() >= event.capacity:
            messages.error(request, "No seats available for this event.")
            return redirect('userviewevent')

        # Save booking, user is None if anonymous
        Booking.objects.create(
            user=request.user if request.user.is_authenticated else None,
            name=name,
            email=email,
            event=event,
            booking_date=timezone.now()
        )
        messages.success(request, f"You have successfully booked '{event.title}'.")
        return redirect('userviewevent')

    return render(request, 'book_event.html', {'event': event})


def userviewreg(request):
    msg = request.GET.get('msg')
    users = UserReg.objects.all()
    return render(request, 'adminusers.html', {"users": users, "msg": msg})
from django.shortcuts import get_object_or_404, redirect
from .models import UserReg  # adjust path based on your app structure

def delete_user(request, id):
    user = get_object_or_404(UserReg, id=id)
    user.delete()
    return redirect('userviewreg')  # or 'userhome' if that's where you want to redirect

from django.shortcuts import get_object_or_404

def delete_event(request, id):
    event = get_object_or_404(Event, id=id)
    event.delete()
    return redirect('addevent')  # or use your actual view name
def update_event(request, id):
    event = get_object_or_404(Event, id=id)
    msg = ''
    if request.method == "POST":
        event.title = request.POST.get("title")
        event.description = request.POST.get("description")
        event.datetime = request.POST.get("datetime")
        event.venue = request.POST.get("venue")
        event.capacity = request.POST.get("capacity")
        event.regdead = request.POST.get("regdead")
        if 'image' in request.FILES:
            event.image = request.FILES['image']
        event.save()
        msg = "Updated Successfully"
        return redirect('addevent')  # back to the add event page

    return render(request, 'update_event.html', {'event': event, 'msg': msg})
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')  # Replace 'login' with the name of your login page URL
from django.contrib.auth.decorators import login_required

@login_required
def user_home(request):
    events = Event.objects.filter(datetime__gte=timezone.now())
    booked_events = Booking.objects.filter(user=request.user).select_related('event')
    return render(request, 'userhome.html', {
        'events': events,
        'booked_events': booked_events,
    })
def userviewevent(request):
    msg = request.GET.get('msg')
    events = Event.objects.filter(datetime__gte=timezone.now())

    user_bookings = []
    if request.user.is_authenticated:
        # Only show bookings if user is logged in
        user_bookings = Booking.objects.filter(user=request.user).values_list('event_id', flat=True)

    return render(request, 'userhome.html', {
        "events": events,
        "user_bookings": user_bookings,  # empty list if not logged in
        "msg": msg
    })




