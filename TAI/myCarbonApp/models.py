from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Page_users(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=12, unique=True)
    password = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to='images')
    date_joined = models.DateTimeField('$date joined', auto_now_add=True)
    def __str__(self):
        return self.username
    def recently_joined(self):
        return self.date_joined >= timezone.localtime(timezone.now()) - datetime.timedelta(days=2)
    class Meta:
        db_table = 'Users'

class Subscribers(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30, unique=True)
    date_subscribed = models.DateTimeField('$date joined')
    def __str__(self):
        return self.email
    def recently_subscribed(self):
        return self.date_subscribed >= timezone.localtime(timezone.now()) - datetime.timedelta(days=1)
    class Meta:
        db_table = 'subscribers'

class InCart(models.Model):
    customer = models.ForeignKey(Page_users, on_delete=models.CASCADE)#figure out how to use foreign keys here
    id = models.BigAutoField(primary_key=True)
    amount = models.PositiveIntegerField()
    offset_type = models.CharField(max_length=200)
    date_cart_entered = models.DateTimeField('$date cart entered', auto_now_add=True)
    def __str__(self):
        return self.customer
    def max_date_in_cart(self):
        #15 days to stay in cart max
        return self.max_date_in_cart() >= timezone.localtime(timezone.now()) - datetime.timedelta(days=15)
    class Meta:
        db_table = 'in_cart'


class CheckedOut(models.Model):
    customer = models.ForeignKey(Page_users, on_delete=models.CASCADE)  # figure out how to use foreign keys here
    id = models.BigAutoField(primary_key=True)
    amount = models.PositiveIntegerField()
    date_checked_out = models.DateTimeField('$date cart entered', auto_now_add=True)
    def __str__(self):
        return self.customer
    class Meta:
        db_table = 'check_out'