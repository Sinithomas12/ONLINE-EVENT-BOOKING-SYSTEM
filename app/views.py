from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Login,Event,UserReg# Adjust the import based on your app
from django.utils import timezone
from app.models import UserReg

def index(request):
    return render(request,'index.html')

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
def addevent(request): 
    title=request.POST.get("title")
    msg=request.GET.get('msg')
    if Event.objects.filter(title=title).exists():
        mg="already added"

    else:
       msg = ""
       msg = request.GET.get('msg')
       if request.POST:
          
           image = request.FILES["image"]
           title=request.POST.get("title")
           description=request.POST.get("description")
           datetime=request.POST.get("datetime")
           venue=request.POST.get("venue")
           capacity=request.POST.get("capacity")
           regdead=request.POST.get("regdead")
           abc = Event.objects.create(
                image=image,title=title,description=description,venue=venue,datetime=datetime,capacity=capacity,regdead=regdead)
           abc.save()
           msg = "Added Successfully"
    events = Event.objects.filter(datetime__gte=timezone.now())
    return render(request, 'adminadd.html', {"msg": msg,'events':events})
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

        # Save booking
        Booking.objects.create(
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



