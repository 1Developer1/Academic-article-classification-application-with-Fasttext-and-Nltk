from django.db import models
from django.contrib.auth.models import User


class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username=models.CharField( max_length=50)
    gender=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    age=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    location=models.CharField(max_length=50)
    interest1=models.CharField( max_length=50)
    interest2=models.CharField( max_length=50)
    interest3=models.CharField( max_length=50)
   
class Article(models.Model):
    filename = models.CharField(max_length=255)
    content = models.TextField()
    vector = models.TextField()
    true_labels = models.TextField()  

def __str__(self):
    return f"{self.full_name}" # bu şekilde yaparak admin
#panelinde username isimleri ile listelenir.
