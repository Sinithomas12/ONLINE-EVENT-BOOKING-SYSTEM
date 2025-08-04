from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from .models import Login, Event, UserReg, Booking

def index(request):
    return render(request, 'index.html')


# ---------------------------
# Authentication Views
# ---------------------------

def login(request):
    msg = request.GET.get('msg', '')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            data = Login.objects.get(email=email, password=password)
            request.session['email'] = email
            request.session['userType'] = data.userType

            if data.userType == "admin":
                return render(request, 'admin.html')
            elif data.userType == "user":
                return redirect('userviewevent')

        except Login.DoesNotExist:
            msg = "Invalid username or password provided"

    return render(request, 'login.html', {'msg': msg})


def logout_view(request):
    request.session.flush()
    return redirect('login')
def logouts(request):
    logouts(request)  # Log out the user
    return redirect('index')

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Login.objects.get(email=email)
            new_password = 'TempPass123'  # insecure - only for demo
            user.password = new_password
            user.save()

            send_mail(
                subject='Password Reset - Event Booking',
                message=f'Your temporary password is: {new_password}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
            messages.success(request, 'Temporary password sent to your email.')
            return redirect('login')
        except Login.DoesNotExist:
            messages.error(request, 'No user found with this email.')

    return render(request, 'forgotpassword.html')


def userreg(request):
    msg = request.GET.get('msg', '')
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        address = request.POST.get("address")
        gender = request.POST.get("gender")

        if UserReg.objects.filter(email=email).exists() or Login.objects.filter(email=email).exists():
            msg = "Email Already Registered"
        else:
            login_obj = Login.objects.create(email=email, password=password, userType='user')
            UserReg.objects.create(name=name, email=email, phone=phone, password=password,
                                   address=address, gender=gender, usrid=login_obj)
            msg = "Registration Successful"
    return render(request, 'userreg.html', {"msg": msg})


# ---------------------------
# Event Views
# ---------------------------

def addevent(request):
    msg = ""

    if request.method == "POST":
        title = request.POST.get("title")

        if Event.objects.filter(title=title).exists():
            msg = "Event with this title already exists."
        else:
            Event.objects.create(
                image=request.FILES.get("image"),
                title=title,
                description=request.POST.get("description"),
                datetime=request.POST.get("datetime"),
                venue=request.POST.get("venue"),
                capacity=request.POST.get("capacity"),
                regdead=request.POST.get("regdead")
            )
            msg = "Event added successfully."

    events = Event.objects.filter(datetime__gte=timezone.now())
    return render(request, 'adminadd.html', {"msg": msg, "events": events})


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
        return redirect('addevent')
    return render(request, 'update_event.html', {'event': event})


def delete_event(request, id):
    event = get_object_or_404(Event, id=id)
    event.delete()
    return redirect('addevent')


# ---------------------------
# User Views
# ---------------------------

def profile_view(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')

    try:
        user_profile = UserReg.objects.get(email=email)
    except UserReg.DoesNotExist:
        user_profile = None

    if request.method == "POST" and user_profile:
        user_profile.name = request.POST.get("name")
        user_profile.phone = request.POST.get("phone")
        user_profile.address = request.POST.get("address")
        user_profile.gender = request.POST.get("gender")
        user_profile.save()

    return render(request, 'profile.html', {
        'user_profile': user_profile
    })


def my_bookings(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')

    bookings = Booking.objects.filter(email=email).select_related('event').order_by('-booking_date')
    return render(request, 'mybookings.html', {'bookings': bookings})


# ---------------------------
# Event Viewing & Booking
# ---------------------------

def userviewevent(request):
    msg = request.GET.get('msg')
    email = request.session.get('email')
    if not email:
        return redirect('login')

    events = Event.objects.filter(datetime__gte=timezone.now(), regdead__gte=timezone.now())

    # Get IDs of events the user already booked
    user_bookings = Booking.objects.filter(email=email).values_list('event_id', flat=True)

    return render(request, 'userhome.html', {
        "events": events,
        "user_bookings": user_bookings,
        "msg": msg
    })


def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")

        if timezone.now() > event.regdead:
            messages.error(request, "Registration deadline has passed.")
            return redirect('userviewevent')

        if Booking.objects.filter(event=event, email=email).exists():
            messages.warning(request, "You have already booked this event.")
            return redirect('userviewevent')

        if Booking.objects.filter(event=event).count() >= event.capacity:
            messages.error(request, "No seats available for this event.")
            return redirect('userviewevent')

        Booking.objects.create(
            name=name,
            email=email,
            event=event,
            booking_date=timezone.now()
        )
        messages.success(request, f"You have successfully booked '{event.title}'.")
        return redirect('userviewevent')

    return render(request, 'book_event.html', {'event': event})


# ---------------------------
# Admin Profile Management
# ---------------------------

def userviewreg(request):
    users = UserReg.objects.all()
    msg = request.GET.get("msg", "")
    return render(request, 'adminusers.html', {'users': users, 'msg': msg})



def delete_user(request, id):
    user = get_object_or_404(UserReg, id=id)
    user.delete()
    return redirect('userviewreg')
