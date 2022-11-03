# from rest_framework import viewsets
from django.db.models import JSONField

# from softdelete.models import SoftDeleteModel
import dashboard
from django.contrib.auth.base_user import BaseUserManager
from restaurant_managment.settings import TIME_ZONE
from django.db import models
from cafe.models import Cafe
from django.contrib.auth.models import AbstractUser, User, UserManager
import uuid
from django.utils import timezone
from random import randint
from django.utils.timezone import timedelta

# Create your models here.



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        # if not username:
        #     raise ValueError('The given username must be set')
        # phone = self.normalize_email(phone)
        username = self.model.normalize_username(username)
        user = self.model(
            # username=username, email=email,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None,  password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class UserAccount(AbstractUser):
    username = None
    phone = None
    last_name = None

    email = models.EmailField(max_length=35, unique=True)
    phone = models.CharField(max_length=35, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]
    objects = UserManager()
    

class CustomerInfo(models.Model):
    GENDER = [
        ("MALE", "Male"),
        ("FEMALE", "Female"),
        ("OTHERS", "Others"),
        ]

    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=35)
    phone = models.CharField(max_length=35)
    total_point = models.FloatField(default=0.0)
    date_of_birthday = models.DateField(null=True, blank=True)
    image = models.FileField(upload_to='customer',
                             null=True, blank=True)
    gender = models.CharField(choices=GENDER,
                              default='MALE',max_length=20)
    user = models.ForeignKey(
        to = UserAccount, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='customers'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# class CustomerLocation(models.Model):
#     city = models.CharField(max_length=255)
#     location = LocationField(based_fields=['city'],
#                              zoom=7, default=Point(1.0, 1.0))
#
#     customer_info = models.ForeignKey(
#         CustomerInfo, on_delete=models.SET_NULL,
#         null=True, blank=True,
#         related_name='customer_locations'
#     )

    # def __str__(self):
    #     return self.city


class CafeStaffInformation(models.Model):
    staff_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=250)
    image = models.FileField(upload_to='cafe_staff',
                             null=True, blank=True)
    cafe = models.ForeignKey(
        Cafe, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='cafe_staff_informations'
    )
    user = models.ForeignKey(
        to= UserAccount, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='cafe_staff_informations'
    )
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=150)
    date_of_birth = models.DateField(null=True, blank=True)
    nid = models.CharField(max_length=100)
    shift_start_hour = models.TimeField(null=True, blank=True)
    shift_end_hour = models.TimeField(null=True, blank=True)
    is_manager = models.BooleanField(default=False)
    is_barista = models.BooleanField(default=False)
    is_delivery_boy = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class StaffFcmDevice(models.Model):
    cafe_staff = models.ForeignKey(
        to=CafeStaffInformation, on_delete=models.CASCADE,
        related_name='staff_fcm_devices')
    device_id = models.CharField(max_length=255, null=True, blank=True)
    token = models.CharField(max_length=255)
    device_type = models.CharField(
        choices=[('web', 'web'), ('ios', 'ios'), ('android', 'android')], default='android', max_length=25)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class CustomerFcmDevice(models.Model):
    customer = models.ForeignKey(
        to=CustomerInfo, on_delete=models.CASCADE,
        related_name='customer_fcm_devices')
    device_id = models.CharField(max_length=255, null=True, blank=True)
    token = models.CharField(max_length=255)
    device_type = models.CharField(
        choices=[('web', 'web'), ('ios', 'ios'),
                 ('android', 'android')],
        default='android', max_length=25)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class FcmNotificationStaff(models.Model):
    staff_device = models.ForeignKey(
        to=StaffFcmDevice, null=True, on_delete=models.SET_NULL)
    data = JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class FcmNotificationCustomer(models.Model):
    customer_device = models.ForeignKey(
        to=CustomerFcmDevice, null=True, on_delete=models.SET_NULL)
    title = models.TextField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    data = JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
