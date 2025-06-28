from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Login,Event# Adjust the import based on your app



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
                  
                    return HttpResponse("user")
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
    events = Event.objects.all().order_by('-datetime')
    return render(request, 'adminadd.html', {"msg": msg,'events':events})