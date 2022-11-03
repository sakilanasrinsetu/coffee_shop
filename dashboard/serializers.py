from dataclasses import field, fields
from .models import *
from rest_framework import serializers
# from drf_extra_fields.fields import Base64FileField, Base64ImageField
from django.utils.html import strip_tags
# from utils.calculate_price import calculate_price
import datetime
from django.utils import timezone
from datetime import datetime
from accounts.models import CustomerInfo
from django.db.models import Q

# BASE_URL = 'http://127.0.0.1:8000/media/'
# BASE_URL = 'http://192.168.20.248:8000/media/'
BASE_URL = 'https://arabikastaging.techsistltd.com/media/'


# ..........***.......... Customer Info Start ..........***..........

# class CustomerInfoSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = CustomerInfo
#         fields = '__all__'