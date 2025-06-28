from django.db import models

# Create your models here.

class Login(models.Model):
    email = models.EmailField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    userType = models.CharField(max_length=100, null=True)


class Event(models.Model):
    title = models.CharField(max_length=255)
    image= models.ImageField(max_length=100, null=True)
    description = models.TextField()
    datetime = models.DateTimeField()
    venue = models.CharField(max_length=255)
    capacity = models.IntegerField()
    regdead = models.DateTimeField()

    def __str__(self):
        return self.title
