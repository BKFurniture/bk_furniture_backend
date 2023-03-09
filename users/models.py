from django.db import models
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='user_avatars')
    phone = PhoneNumberField(blank=True, null=True)
    address = models.CharField(max_length=511, blank=True, null=True)
