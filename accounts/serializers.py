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

from drf_extra_fields.fields import Base64ImageField

from dataclasses import field
from accounts.models import *
from rest_framework import serializers, validators


# BASE_URL = 'http://127.0.0.1:8000/media/'
BASE_URL = 'http://192.168.1.16:8000/media/'
# BASE_URL = 'https://arabikastaging.techsistltd.com/media/'


# ..........***.......... Cafe Staff Info Start ..........***..........

class SocialAuthTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerInfo
        fields = ['email']

# ..........***.......... Cafe Staff Info Start ..........***..........

class CafeStaffInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CafeStaffInformation
        fields = '__all__'


# ..........***.......... Customer Info Start ..........***..........


class CustomerInfoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomerInfo
        # fields = '__all__'
        exclude = ['user']

    def get_image_url(self, obj):
        if obj.image:
            file_name = obj.image
            return BASE_URL + str(file_name)
        else:
            return None


class CustomerInfoUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerInfo
        # fields = '__all__'
        exclude = ['user', 'email', 'phone']


class CustomerInfoUpdateWithSocialMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerInfo
        # fields = '__all__'
        exclude = ['user']


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAccount
        fields = [
            'email',
            'phone',
            'password',
            ]


class UserDetailsSerializer(serializers.ModelSerializer):
    customer_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserAccount
        fields = [
            'id',
            'email',
            'customer_info',
        ]

    def get_customer_info(self, obj):
        if obj:
            serializer = CustomerInfoSerializer(obj.customers.last())
            return serializer.data
        return


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    is_superuser = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserAccount
        fields = [
            'id',
            'email',
            'name',
            'phone',
            'is_superuser'
        ]

    def get_name(self, obj):
        return 'Taseen Bappi'


    def get_is_superuser(self, obj):
        return True


class CafeStaffInformationSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)
    cafe_deatils = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CafeStaffInformation
        fields = '__all__'

    def get_image_url(self, obj):
        a ='vd'
        if obj.image:
            file_name = obj.image
            return BASE_URL + str(file_name)
        else:
            return None

    def get_cafe_deatils(self, obj):
        if obj.cafe:
            return {
                'id': obj.cafe.id,
                'name': obj.cafe.name,
                'address': obj.cafe.address,
                'email': obj.cafe.email,
                'phone': obj.cafe.phone,
                'is_active': obj.cafe.is_active,
            }
        else:
            return None


class EmployeeCreateSerializer(serializers.Serializer):
    # image = Base64ImageField()
    staff_id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    cafe_id = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=True)
    nid = serializers.CharField(required=True)
    shift_start_hour = serializers.TimeField(required=True)
    shift_end_hour = serializers.TimeField(required=True)
    is_active = serializers.BooleanField(required=True)
    password = serializers.CharField(required=True)

    # def create(self, validated_data):
    #     image = validated_data.pop('image', None)
    #     if image:
    #         return CafeStaffInformation.objects.create(image=image, **validated_data)
    #     return CafeStaffInformation.objects.create(**validated_data)
    #


class StaffInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CafeStaffInformation
        fields = [
            'staff_id',
            'name',
            'image',
            'cafe',
            'email',
            'phone',
            'date_of_birth',
            'nid',
            'shift_start_hour',
            'shift_end_hour',
            'is_active',
        ]

    def create(self, validated_data):
        image = validated_data.pop('image', None)
        if image:
            return CafeStaffInformation.objects.create(image=image, **validated_data)
        return CafeStaffInformation.objects.create(**validated_data)
    

class EmailCheckSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)



class CustomerFcmDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerFcmDevice
        fields = "__all__"