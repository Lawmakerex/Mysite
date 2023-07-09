from django.db import models

from models.phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class UserProfile(models.Model):
    image = models.ImageField(upload_to="images")
    
    
class User(ABstractUser):
    phone_number = PhoneNumberField()