from django.db import models
from django.contrib.auth.models import AbstractBaseUser




class User(AbstractBaseUser):
    phonenumber=models.CharField(max_length=12, unique=True)



# Create your models here.
class carosuel(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    image1 = models.ImageField(upload_to='carosuel',null=False, blank=False)
    title = models.CharField(max_length=200, null=False, blank=False)
    status=models.BooleanField(default=False,help_text="0=default,1=Hidden")
    description = models.TextField()

    def __str__(self):
        
        return self.name

