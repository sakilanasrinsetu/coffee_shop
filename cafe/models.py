from django.db import models
from django.contrib.auth.models import Group, Permission, User
from util.helpers import get_dynamic_fields
from util.utils import (
    time_str_mix_slug)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify

import uuid

# Create your models here.


# ............***............ Cloud Cafe Information ............***............


class CloudCafeInformation(models.Model):
    name = models.CharField(max_length=250)
    logo = models.FileField(upload_to='logo',
                            null=True, blank=True)
    address = models.CharField(max_length=550)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    vat_registration_number = models.CharField(max_length=100)
    vat_amount = models.FloatField(default=0.0)
    delivery_amount = models.FloatField(default=0.0)
    facebook_url = models.CharField(max_length=500,
                                    null=True, blank=True)
    instagram_url = models.CharField(max_length=500,
                                     null=True, blank=True)
    youtube_url = models.CharField(max_length=500,
                                   null=True, blank=True)

    def __str__(self):
        return self.name


# ............***............ Cafe ............***............


class Cafe(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=550)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ............***............ Notification ............***............


class Notification(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='notification', null=True,
                              blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ............***............ Category ............***............


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=350)
    image = models.FileField(upload_to='category',
                             null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ............***............ Food ............***............


class Food(models.Model):
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=100,
                                 null=True, blank=True)
    slug = models.CharField(max_length=350)
    image = models.FileField(upload_to='food',
                             null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='foods'
    )
    cafe = models.ManyToManyField(
        Cafe, blank=True, related_name='foods')
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_vat_applicable = models.BooleanField(default=True)
    order_counter = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    total_rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ............***............ Food Option ............***............


class FoodOption(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField(default=0.0)
    food = models.ForeignKey(
        Food, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='food_options'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ............***............ Food Extra ............***............


class FoodExtra(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField(default=0.0)
    food = models.ForeignKey(
        Food, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='food_extras'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ............***............ Food Order ............***............


class FoodOrder(models.Model):
    ORDER_STATUS = [
        ("ORDER_PLACED", "Order Confirm"),
        ("PREPARING", "Preparing"),
        ("PICKED", "Picked Up"), # From Delivery APP
        ("ON_THE_WAY", "On the Way"), # From Delivery APP
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ]
    order_no = models.CharField(max_length=50, unique=True)
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(choices=ORDER_STATUS,
                              default='USER_CONFIRMED',
                              max_length=50)
    grand_total = models.FloatField(default=0.0,
                                    null=True, blank=True)
    vat_amount = models.FloatField(default=0.0,
                                   null=True, blank=True)
    payable_amount = models.FloatField(default=0.0,
                                       null=True, blank=True)
    customer = models.ForeignKey(to='accounts.CustomerInfo',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 related_name='food_orders')
    cafe = models.ForeignKey(Cafe,
                             on_delete=models.SET_NULL,
                             null=True, blank=True,
                             related_name='food_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_no


# ............***............ Food Order Log ............***............

class FoodOrderLog(models.Model):
    order = models.ForeignKey(FoodOrder,
                              on_delete=models.SET_NULL,
                              null=True, blank=True,
                              related_name='food_order_logs')
    staff = models.ForeignKey(to="accounts.CafeStaffInformation",
                              on_delete=models.SET_NULL, null=True,blank=True,
                              related_name='food_order_logs')
    order_status = models.CharField(max_length=50)
    pickup_time_at = models.DateTimeField(null=True, blank=True)
    on_the_way_time_at = models.DateTimeField(null=True, blank=True)
    delivered_time_at = models.DateTimeField(null=True, blank=True)
    distance = models.FloatField(default=0.0)
    total_time = models.CharField(max_length=50, null=True, blank=True)  # Convert into Minutes = (delivered_time_at - pickup_time_at)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


# ............***............ Order Item ............***............

class OrderedItem(models.Model):
    ITEM_STATUS = [
        ("ORDER_PLACED", "User Confirmed"),
        ("PREPARING", "Preparing"),
        ("PICKED", "Picked"),
        ("ON_THE_WAY", "On the Way"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ]
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    food_option = models.ForeignKey(
        FoodOption, on_delete=models.PROTECT, related_name='ordered_items')
    food_extra = models.ManyToManyField(
        FoodExtra, blank=True, related_name='ordered_items')
    food_order = models.ForeignKey(
        FoodOrder, on_delete=models.CASCADE, related_name='ordered_items')
    status = models.CharField(
        choices=ITEM_STATUS, default="ORDER_PLACED", max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    # def __str__(self):
    #     return self.food_option.title


# ............***............ Invoice ............***............

class Invoice(models.Model):
    STATUS = [
        ("PAID", "Paid"),
        ("UNPAID", "Unpaid")
    ]
    id = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4)
    cafe = models.ForeignKey(Cafe, on_delete=models.SET_NULL,
                             null=True, blank=True, related_name='invoices')
    order = models.ForeignKey(FoodOrder, null=True,
                              blank=True, on_delete=models.SET_NULL,
                              related_name='invoices')
    grand_total = models.FloatField(default=0.0,
                                    null=True, blank=True)
    vat_amount = models.FloatField(default=0.0,
                                   null=True, blank=True)
    payable_amount = models.FloatField(default=0.0,
                                       null=True, blank=True)
    payment_status = models.CharField(
        choices=STATUS, max_length=25, default="UNPAID")
    order_info = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


# ............***............ Review ............***............

class Review(models.Model):
    order = models.ForeignKey(FoodOrder,
                              on_delete=models.SET_NULL,
                              null=True, blank=True,
                              related_name='reviews')
    customer = models.ForeignKey(to='accounts.CustomerInfo',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order)
    

# ............***............ WishList ............***............
 
 
class WishList(models.Model): 
    food = models.ForeignKey(Food, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='wish_lists'
    )
    
    customer = models.ForeignKey(to='accounts.CustomerInfo', on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name='wish_lists')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.food)
# ............***............ Category ............***............


def category_slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        title = slugify(instance.title.lower()[:17])
        slug_binding = title + '-' + time_str_mix_slug()
        instance.slug = slug_binding


pre_save.connect(category_slug_pre_save_receiver, sender=Category)


# ............***............ Food ............***............


def food_slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        title = slugify(instance.title.lower()[:17])
        slug_binding = title + '-' + time_str_mix_slug()
        instance.slug = slug_binding


pre_save.connect(food_slug_pre_save_receiver, sender=Food)
