"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('login',views.login,name="login"),
    path('events', views.addevent, name='addevent'), 
    path('userreg', views.userreg, name='userreg'), 
    path('userviewevent', views.userviewevent, name='userviewevent'), 
    path('book/<int:event_id>/', views.book_event, name='book_event'),
    path('userviewreg', views.userviewreg, name='userviewreg'), 
    path('deleteevent/<int:id>/', views.delete_event, name='delete_event'), 
    path('updateevent/<int:id>/', views.update_event, name='update_event'),
    path('logout/', views.logout_view, name='logout'),
    path('userreg', views.userreg, name='userreg'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'static'))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
