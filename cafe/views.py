from django.shortcuts import render
from utils.custom_viewset import CustomViewSet
from utils.custom_permissions import *

from utils.response_wrapper import ResponseWrapper
from .serializers import *
from .models import *
from accounts.models import *
from dashboard.models import *
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from datetime import datetime
from django.utils import timezone
import datetime
import random
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import permissions, status, viewsets
import json
from django.db.models import Q


from utils.fcm import send_fcm_push_notification_appointment


from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password
from drf_yasg2.utils import swagger_auto_schema
from django.contrib.auth import get_user_model, login
import base64
import codecs


from django.conf import settings
# Create your views here.


class FoodOrderCore:
    def invoice_generator(self, food_order_qs, payment_status, *args, **kwargs):
        serializer = FoodOrderDetailSerializer(instance=food_order_qs)
        grand_total = serializer.data.get(
            'price', {}).get('grand_total_price')
        payable_amount = serializer.data.get(
            'price', {}).get('payable_amount')

        if food_order_qs.invoices.first():
            invoice_qs = food_order_qs.invoices.first()
            invoice_qs.order_info = json.loads(
                json.dumps(serializer.data, cls=DjangoJSONEncoder))
            invoice_qs.grand_total = food_order_qs.grand_total,
            invoice_qs.payment_status = payment_status
            invoice_qs.payable_amount = food_order_qs.payable_amount
            invoice_qs.vat_amount = food_order_qs.vat_amount
            invoice_qs.save()
        else:
            invoice_qs = Invoice.objects.create(
                cafe_id = food_order_qs.cafe.id,
                order=food_order_qs,
                order_info=json.loads(json.dumps(
                    serializer.data, cls=DjangoJSONEncoder)),
                grand_total=food_order_qs.grand_total,
                payable_amount=food_order_qs.payable_amount,
                vat_amount=food_order_qs.vat_amount,
                payment_status=payment_status
            )
        return invoice_qs

# ............***............ CloudCafeInformation ............***............


class CloudCafeInformationViewSet(CustomViewSet):
    serializer_class = CloudCafeInformationSerializer
    queryset = CloudCafeInformation.objects.all()
    lookup_field = 'pk'
    
    def cloud_cafe_information_details(self, request, *args, **kwargs):
        cloud_cafe_information_qs = CloudCafeInformation.objects.all().last()
        if not cloud_cafe_information_qs:
            return ResponseWrapper(error_msg='cloud cafe information Details Not Found', status=400)
        serializer = CloudCafeInformationSerializer(instance=cloud_cafe_information_qs)
        return ResponseWrapper(data=serializer.data, status=200)   

    def cloud_cafe_information_create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        qs = CloudCafeInformation.objects.all().last()
        if qs:
            return ResponseWrapper(error_msg='cloud cafe information Already created', status=400)
        if serializer.is_valid():
            qs = serializer.save()
            return ResponseWrapper(data=serializer.data, msg='created', status=200)

    def cloud_cafe_information_update(self, request, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            qs = serializer.update(instance=self.get_object(
            ), validated_data=serializer.validated_data)
            serializer = self.serializer_class(instance=qs)
            return ResponseWrapper(data=serializer.data, status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, status=400)


# ............***............ Cafe ............***............


class CafeViewSet(CustomViewSet):
    serializer_class = CafeSerializer
    queryset = Cafe.objects.all()
    lookup_field = 'pk'
    
    def get_serializer_class(self):
        if self.action in ['cafe_custom_update']:
            self.serializer_class = CafeCustomSerializer
        return self.serializer_class

    def get_permissions(self):
        permission_classes = []
        if self.action in ["cafe_create", "cafe_update"]:
            permission_classes = [IsSuperAdminOrAdmin]
        elif self.action in ["cafe_custom_update"]:
            permission_classes = [IsCafeManagerOrAdmin]    
        else:
            # permissions.DjangoObjectPermissions.has_permission()
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
                
    def cafe_create(self, request, *args, **kwargs):
        name = request.data.get('name')
        address = request.data.get('address')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        email = request.data.get('email')
        phone = request.data.get('phone')
        is_active = request.data.get('is_active')
        cafe_qs = Cafe.objects.filter(name=name).exists()
        if cafe_qs:
            return ResponseWrapper(data="Please use different Name, already it has been used", status=400)
        qs = Cafe.objects.create(name = name, address= address, latitude=latitude, longitude=longitude,
                                 email = email, phone = phone, is_active=is_active)
        
        serializer = CafeSerializer(instance=qs)
        return ResponseWrapper(data=serializer.data, status=200)    
    
    def cafe_update(self, request, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            qs = serializer.update(instance=self.get_object(
            ), validated_data=serializer.validated_data)
            serializer = self.serializer_class(instance=qs)
            return ResponseWrapper(data=serializer.data, status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, status=400)


    def cafe_details(self, request,pk, *args, **kwargs):
        cafe_qs = Cafe.objects.filter(id = pk).last()
        if not cafe_qs:
            return ResponseWrapper(error_msg='Cafe Details Not Found', status=400)
        serializer = CafeSerializer(instance=cafe_qs)
        return ResponseWrapper(data=serializer.data, status=200) 
    
    def cafe_list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance = qs, many = True)
        return ResponseWrapper(data = serializer.data, msg='Success', status=200)
    
   
    def cafe_delete(self, request, **kwargs):
        qs = self.queryset.filter(**kwargs).first()
        if qs:
            qs.delete()
            return ResponseWrapper(status=200, msg='deleted')
        else:
            return ResponseWrapper(error_msg="failed to delete", status=400)

    def active_cafe_list(self,request, *args, **kwargs):
        qs = Cafe.objects.filter(is_active = True)
        if not qs:
            return ResponseWrapper(error_msg='No Cafe is avliable now', status=400)
        serializer = CafeSerializer(instance=qs, many=True)
        return ResponseWrapper(data=serializer.data, msg='Success', status=200)

    def cafe_custom_update(self, request, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            qs = serializer.update(instance=self.get_object(
            ), validated_data=serializer.validated_data)
            serializer = self.serializer_class(instance=qs)
            return ResponseWrapper(data=serializer.data, status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, status=400)    
       
   
# ............***............ Category ............***............


class CategoryViewSet(CustomViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'pk'
    
    # def get_permissions(self):
    #     permission_classes = []
    #     if self.action in ["category_create", "category_update"]:
    #         permission_classes = [IsSuperAdminOrAdmin]
    #
    #     elif self.action in ["all_food_list"]:
    #         permission_classes = [permissions.IsAuthenticated]
    #
    #     else:
    #         # permissions.DjangoObjectPermissions.has_permission()
    #         # permission_classes = [permissions.AllowAny]
    #         permission_classes = [permissions.IsAuthenticated]
    #
    #     return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action in ['category_wise_food_list']:
            self.serializer_class = FoodDetailSerializer  
        return self.serializer_class  
                
    def category_create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            qs = serializer.save()
            return ResponseWrapper(data=serializer.data, msg='Category created', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, status=400)
    
    def category_update(self, request, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            qs = serializer.update(instance=self.get_object(
            ), validated_data=serializer.validated_data)
            serializer = self.serializer_class(instance=qs)
            return ResponseWrapper(data=serializer.data, status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, status=400)

    def category_details(self, request, *args, **kwargs):
        category_qs = Category.objects.all().last()
        if not category_qs:
            return ResponseWrapper(error_msg='Category Details Not Found', status=400)
        serializer = CategorySerializer(instance=category_qs)
        return ResponseWrapper(data=serializer.data, status=200)   

    def category_list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = CategorySerializer(instance = qs, many = True)
        return ResponseWrapper(data = serializer.data, msg='Success', status=200)

    def all_food_list(self, request, *args, **kwargs):
        qs = Category.objects.all()
        serializer = CategoryDetailsSerializer(instance = qs, many = True)
        return ResponseWrapper(data = serializer.data, msg='Success', status=200)

    def category_delete(self, request, **kwargs):
        qs = self.queryset.filter(**kwargs).first()
        if qs:
            qs.delete()
            return ResponseWrapper(status=200, msg='deleted')
        else:
            return ResponseWrapper(error_msg="failed to delete", status=400)
       
    def category_wise_food_list(self, request, slug, *args, **kwargs):
        food_qs = Food.objects.filter(category__slug = slug)
        if not food_qs:
            return ResponseWrapper(error_msg='Food details not found', status=400)
        serializer = FoodDetailSerializer(instance=food_qs, many=True)
        return ResponseWrapper(data= serializer.data, status=200)
    
    
# ............***............ Notification ............***............


class NotificationViewSet(CustomViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    lookup_field = 'pk'
                
    def notification_create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            qs = serializer.save()
            return ResponseWrapper(data=serializer.data,
                                   msg='Notification created', status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, status=400)   

    def notification_update(self, request, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            qs = serializer.update(instance=self.get_object(
            ), validated_data=serializer.validated_data)
            serializer = self.serializer_class(instance=qs)
            return ResponseWrapper(data=serializer.data, status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, status=400)    

    def notification_details(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ResponseWrapper(serializer.data, status=200)    

    def notification_list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance = qs, many = True)
        return ResponseWrapper(data = serializer.data, msg='Success',
                               status=200)

    def notification_delete(self, request, **kwargs):
        qs = self.queryset.filter(**kwargs).first()
        if qs:
            qs.delete()
            return ResponseWrapper(status=200, msg='deleted')
        else:
            return ResponseWrapper(error_msg="failed to delete", status=400)   
              

# ............***............ Food ............***............


class FoodViewSet(CustomViewSet):
    serializer_class = FoodDetailSerializer
    queryset = Food.objects.all()
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.action in ['food_create']:
            self.serializer_class = FoodCreateSerializer
        elif self.action in ['food_update']:
            self.serializer_class = FoodUpdateSerializer
        return self.serializer_class

    # def get_permissions(self):
    #     permission_classes = []
    #     if self.action in ["all_food_list"]:
    #         permission_classes = [permissions.IsAuthenticated]
    #     else:
    #         # permissions.DjangoObjectPermissions.has_permission()
    #         # permission_classes = [permissions.AllowAny]
    #         permission_classes = [permissions.IsAuthenticated]
    #
    #     return [permission() for permission in permission_classes]

    def food_search(self, request, title,  *args, **kwargs):
        qs = Food.objects.filter(Q(title__icontains = title) |
                                 Q(category__title__icontains = title)
                                 | Q(food_options__title = title)
                                 | Q(food_extras__title = title)).distinct()

        serializer = FoodDetailSerializer(instance=qs, many=True)
        return ResponseWrapper(data=serializer.data, status=200)
      
    def food_create(self, request, *args, **kwargs):
        title = request.data.get('title')
        image = request.data.get('image')
        sub_title = request.data.get('sub_title')
        category = request.data.get('category')
        description = request.data.get('description')
        is_active = request.data.get('is_active')
        is_vat_applicable = request.data.get('is_vat_applicable')
        food_option_list = request.data.get('food_option')
        food_extra_list = request.data.get('food_extra')
       
        # image = request.data.get('image')
        # b64Str = codecs.encode(str(image))
        # resStr = base64.b64decode(b64Str)
        # print(resStr) # Expected output: "Hello, world!" 
                           
        category_qs = Category.objects.filter(id=category).last()
        if not category_qs:
            return ResponseWrapper(error_msg='Category Not Found', status=400)
        food_qs = Food.objects.filter(title = title, category_id = category_qs.id).last()
        # if food_qs:
        #     return ResponseWrapper(error_msg='Food is already Found', status=400)

        qs = Food.objects.create(title = title, sub_title= sub_title,
                                 category_id = category_qs.id, description = description,
                                 is_active=is_active, is_vat_applicable= is_vat_applicable)
        
        for food_option in food_option_list:
            title = food_option.get('title')
            price = food_option.get('price')
            food_option_qs = FoodOption.objects.create(
                title=title, price = price,
                food_id = qs.id
            )

        for food_extra in food_extra_list:
            title = food_extra.get('title')
            price = food_extra.get('price')
            food_extra_qs = FoodExtra.objects.create(
                title=title, price = price,
                food_id = qs.id
            )   

        serializer = FoodDetailSerializer(instance=qs)
        return ResponseWrapper(data=serializer.data, status=200)
    
    

    def food_update(self, request, pk, **kwargs):
        food_qs = Food.objects.filter(id=pk).last()
        title = request.data.get('title')
        if not title:
            title = food_qs.title

        sub_title = request.data.get('sub_title')
        if not sub_title:
            sub_title = food_qs.sub_title

        category = request.data.get('category')
        if not category:
            category_qs = food_qs.category

        else:
            category_qs = Category.objects.filter(id = category).last()
            if not category_qs:
                return ResponseWrapper(status = 400)

        description = request.data.get('description')
        if not description:
            description = food_qs.description

        is_active = request.data.get('is_active')
        if not is_active:
            is_active = food_qs.is_active

        is_vat_applicable = request.data.get('is_vat_applicable')
        if not is_vat_applicable:
            is_vat_applicable = food_qs.is_vat_applicable

        if food_qs:
            food_qs.title = title
            food_qs.sub_title = sub_title
            food_qs.category_id = category_qs.id
            food_qs.description = description
            food_qs.is_active = is_active
            food_qs.is_vat_applicable = is_vat_applicable
            food_qs.save()

        food_option_list = request.data.get('food_option')
        if food_option_list:
            for food_option in food_option_list:
                id = food_option.get('id')
                food_option_qs = FoodOption.objects.filter(id=id).last()
                if not food_option_qs:
                    return ResponseWrapper(error_msg='Food Option not Found')

                title = request.data.get('title')
                if not title:
                    title = food_option_qs.title

                price = request.data.get('price')
                if not price:
                    price = food_option_qs.price

                if food_option_qs:
                    food_option_qs.title = title
                    food_option_qs.price = price
                    food_option_qs.save()

        food_extra_list = request.data.get('food_extra')

        if food_extra_list:

            for food_extra in food_extra_list:
                id = food_extra.get('id')
                food_extra_qs = FoodOption.objects.filter(id=id).last()
                if not food_extra_qs:
                    return ResponseWrapper(error_msg='Food Extra not found')

                title = request.data.get('title')
                if not title:
                    title = food_extra_qs.title

                price = request.data.get('price')
                if not price:
                    price = food_extra_qs.price

                if food_extra_qs:
                    food_extra_qs.title = title
                    food_extra_qs.price = price
                    food_extra_qs.save()

        serializer = FoodDetailSerializer(instance=food_qs)
        return ResponseWrapper(data=serializer.data, status=200)

    def food_all_details(self, request, slug, *args, **kwargs):
        qs = Food.objects.filter(slug = slug).last()
        if not qs:
            return ResponseWrapper(error_msg='Food Not Found', status=400)
        serializer = FoodDetailSerializer(instance=qs)
        return ResponseWrapper(data=serializer.data, status=200)

    def food_details(self, request, slug, *args, **kwargs):
        qs = Food.objects.filter(slug = slug).last()
        if not qs:
            return ResponseWrapper(error_msg='Food Not Found', status=400)
        serializer = FoodDetailSerializer(instance=qs)
        return ResponseWrapper(data=serializer.data, status=200)

    def recommended_food_list(self, request, *args, **kwargs):
        qs = Food.objects.all().order_by('?')[:5]
        if not qs:
            return ResponseWrapper(error_msg='Food Not Found', status=400)
        serializer = FoodDetailSerializer(instance=qs, many=True)
        return ResponseWrapper(data=serializer.data, status=200)

    def all_food_list(self, request,cafe_id, *args, **kwargs):
        qs = Food.objects.filter(cafe = cafe_id)
        if not qs:
            return ResponseWrapper(error_msg='Food Not Found', status=400)
        serializer = FoodDetailSerializer(instance=qs, many=True)
        return ResponseWrapper(data=serializer.data, status=200)


# ............***............ Review ............***............


class ReviewViewSet(CustomViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    lookup_field = 'pk'
    
    # def get_serializer_class(self):
    #     if self.action in ['category_wise_food_list']:
    #         self.serializer_class = FoodDetailSerializer  
    #     return self.serializer_class

    def review_create(self, request, *args, **kwargs):
        order = request.data.get('order')
        rating = request.data.get('rating')
        review_text = request.data.get('review_text')
        customer = request.data.get('customer')
        food_order_qs = FoodOrder.objects.filter(id=order).last()
        if not food_order_qs:
            return ResponseWrapper(error_msg='Food Order Not Found', status=400)
        for order_item in food_order_qs.ordered_items.all():
            food_qs = order_item.food_option.food

            food_qs.order_counter += 1
            food_qs.total_rating += rating
            food_qs.rating = food_qs.total_rating / food_qs.order_counter
            food_qs.save()

        # customer_qs = CustomerInfo.objects.filter(id=customer).last()
        # if customer_qs:
        #     return ResponseWrapper(error_msg='Customer Info is already Found', status=400)

        qs = Review.objects.create(order_id=food_order_qs.id,
                                   rating=rating, review_text=review_text)
        serializer = ReviewSerializer(instance=qs)
        return ResponseWrapper(data=serializer.data, status=200)

    def review_update(self, request, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            qs = serializer.update(instance=self.get_object(
            ), validated_data=serializer.validated_data)
            serializer = self.serializer_class(instance=qs)
            return ResponseWrapper(data=serializer.data, status=200)
        else:
            return ResponseWrapper(error_msg=serializer.errors, status=400)    

    def review_details(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return ResponseWrapper(serializer.data, status=200)   

    def review_list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance = qs, many = True)
        return ResponseWrapper(data = serializer.data, msg='Success', status=200)

    def cafe_wise_review_list(self, request,cafe_id, *args, **kwargs):
        qs = Review.objects.filter(order__cafe_id = cafe_id)

        serializer = ReviewSerializer(instance = qs, many = True)
        return ResponseWrapper(data = serializer.data, msg='Success', status=200)

    def review_delete(self, request, **kwargs):
        qs = self.queryset.filter(**kwargs).first()
        if qs:
            qs.delete()
            return ResponseWrapper(status=200, msg='deleted')
        else:
            return ResponseWrapper(error_msg="failed to delete", status=400)   

    def list(self, request, *args, **kwargs):
        qs = Food.objects.all().order_by('-created_at')
        if not qs:
            return ResponseWrapper(error_msg='Food List Not Found', status=400)
        serializer = FoodDetailSerializer(instance=qs, many=True)
        return ResponseWrapper(data=serializer.data, status=200)

    def available_food_list(self, request, *args, **kwargs):
        qs = Food.objects.filter(is_active= True).order_by('-created_at')
        if not qs:
            return ResponseWrapper(error_msg='Food List Not Found', status=400)
        serializer = FoodDetailSerializer(instance=qs, many=True)
        return ResponseWrapper(data=serializer.data, status=200)


# ............***............ Food Order............***............


class FoodOrderViewSet(CustomViewSet, FoodOrderCore):
    serializer_class = FoodDetailSerializer
    queryset = FoodOrder.objects.all()
    lookup_field = 'pk'
    
    def get_permissions(self):
        permission_classes = []
        if self.action in ["all_order_running_order_list",
                           ]:
            permission_classes = [permissions.IsAdminUser]

        elif self.action in ['food_order_create', "customer_order_history_list"]:
            permission_classes = [permissions.IsAuthenticated]

        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ['food_order_create']:
            self.serializer_class = FoodOrderCreateSerializer
        elif self.action in ['food_order_preparing','food_order_cancel','food_order_delivered','food_order_on_the_way']:
            self.serializer_class = FoodOrderPreparingSerializer
        elif self.action in ['food_order_picked']:
            self.serializer_class = FoodOrderPickedSerializer
        elif self.action in ['order_item_cancel']:
            self.serializer_class = OrderItemCancelSerializer
        elif self.action in ['food_reorder_create']:
            self.serializer_class = FoodOrderPreparingSerializer    
        return self.serializer_class

    def running_order_list(self, request, cafe_id, *args, **kwargs):
        qs = FoodOrder.objects.filter(cafe_id =cafe_id).exclude(
            status__in = ['INVOICE','CANCELLED']).order_by('id')
        if not qs:
            return ResponseWrapper(error_msg='No Order is Running Now',
                                   status=400)
        serializer = FoodOrderDetailSerializer(instance=qs, many=True)
        return ResponseWrapper(data=serializer.data, status=200)

    def total_running_order_list(self, request, cafe_id, *args, **kwargs):
        qs = FoodOrder.objects.filter(cafe_id =cafe_id).exclude(
            status__in = ['INVOICE','CANCELLED']).order_by('id')
        if not qs:
            return ResponseWrapper(error_msg='No Order is Running Now',
                                   status=400)
        total_confirm_order = qs.filter(status = 'ORDER_PLACED').count()
        total_preparing_order = qs.filter(status = 'PREPARING').count()
        total_picked_order = qs.filter(status = 'PICKED').count()
        total_delivered_order = qs.filter(status = 'DELIVERED').count()
        return ResponseWrapper(
            data=
            {
                'total_confirm_order': total_confirm_order,
                'total_preparing_order': total_preparing_order,
                'total_picked_order': total_picked_order,
                'total_delivered_order': total_delivered_order,
            },
            status=200)

    def food_order_details(self, request, id, *args, **kwargs):
        qs = FoodOrder.objects.filter(id =id).last()
        if not qs:
            return ResponseWrapper(error_msg='Order Not Found', status=400)
        serializer = FoodOrderDetailSerializer(instance=qs)
        return ResponseWrapper(data=serializer.data, status=200)

    def food_order_create(self, request, *args, **kwargs):
    
        random_num = random.randint(348, 965)
        today = timezone.now()

        remarks = request.data.get('remarks')
        # cafe = request.data.get('cafe')
        order_item_list = request.data.get('order_item')

        # cafe_qs = Cafe.objects.filter(id = cafe).last()

        cafe_qs = Cafe.objects.all().first()
        if not cafe_qs:
            return ResponseWrapper(error_msg='Cafe Not Found', status=400)

        food_order_qs = FoodOrder.objects.all().last()

        order_no = '#AC' + str(random_num) + str(food_order_qs.id+1)

        customer_info = CustomerInfo.objects.filter(user = self.request.user).last()

        customer_food_order_qs = FoodOrder.objects.filter(customer_id = customer_info).last()
        
        if customer_food_order_qs:

            if not customer_food_order_qs.status == 'DELIVERED':
                return ResponseWrapper(error_msg='Food Order is Already Running',
                                       status=400)

        food_order_qs = FoodOrder.objects.create(
            remarks= remarks, cafe_id = cafe_qs.id,
            status = 'ORDER_PLACED',order_no = order_no,
            customer_id =customer_info.id
        )

        for order_item in order_item_list:
            quantity = order_item.get('quantity')
            food_option = order_item.get('food_option')
            food_extra_list = order_item.get('food_extra')
            food_option_qs = FoodOption.objects.filter(id = food_option).last()
            if not food_option_qs:
                return ResponseWrapper(error_msg='Food Option Not Found',
                                       status=400)

            order_item_qs = OrderedItem.objects.create(
                quantity = quantity, food_option_id = food_option_qs.id,
                status = 'ORDER_PLACED', food_order_id = food_order_qs.id
            )

            for food_extra in food_extra_list:
                food_extra_qs = FoodExtra.objects.filter(id=food_extra).last()
                order_item_qs.food_extra.add(food_extra_qs.id)

        serializer = FoodOrderDetailSerializer(instance=food_order_qs)
        return ResponseWrapper(data=serializer.data, status=200)

    def food_order_preparing(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')

        food_order_qs = FoodOrder.objects.filter(id = order_id).last()

        if not food_order_qs:
            return ResponseWrapper(error_msg='Food Order Not Found',
                                   status=400)

        if not food_order_qs.status == 'ORDER_PLACED':
            return ResponseWrapper(error_msg='Food Order is Already Preparing',
                                   status=400)

        food_order_qs.status = 'PREPARING'
        food_order_qs.save()

        food_order_qs.ordered_items.update(status="PREPARING")

        serializer = FoodOrderDetailSerializer(instance=food_order_qs)
        return ResponseWrapper(data=serializer.data, status=200)

    def food_order_cancel(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        food_order_qs = FoodOrder.objects.filter(id = order_id,
                                                 status__in=['ORDER_PLACED','PREPARING','PICKED']).last()

        if not food_order_qs:
            return ResponseWrapper(error_msg='Food Order Not Found',
                                   status=400)

        food_order_qs.status = 'CANCELLED'
        food_order_qs.save()

        food_order_qs.ordered_items.update(status="CANCELLED")

        customer_fcm_device_qs = CustomerFcmDevice.objects.filter(
            customer__food_orders__id=food_order_qs.pk
        )

        # customer_id = customer_fcm_device_qs.values_list('pk').last()

        if send_fcm_push_notification_appointment(
                tokens_list=list(
                    customer_fcm_device_qs.values_list('token', flat=True)),
                status='OrderCancel',
                order_no=food_order_qs.order_no
        ):
            pass
        serializer = FoodOrderDetailSerializer(instance=food_order_qs)
        return ResponseWrapper(data=serializer.data, status=200)

    def food_order_picked(self, request, *args, **kwargs):
        today = timezone.now()
        order_id = request.data.get('order_id')

        delivery_boy_id = request.data.get('delivery_boy_id')

        staff_qs = CafeStaffInformation.objects.filter(id = delivery_boy_id,
                                                       is_delivery_boy=True).last()

        if not staff_qs:
            return ResponseWrapper(error_msg='Delivery Boy Not Found',
                                   status=400)

        food_order_qs = FoodOrder.objects.filter(id = order_id,
                                                 status__in=['PREPARING']).last()

        if not food_order_qs:
            return ResponseWrapper(error_msg='Food Order Not Found',
                                   status=400)

        food_order_log_qs = FoodOrderLog.objects.filter(order_id = order_id).last()

        if food_order_log_qs:
            return ResponseWrapper(error_msg='Food Order Already Delivered',
                                   status=400)

        food_order_log_qs = FoodOrderLog.objects.create(
            order_id = food_order_qs.id, staff_id = staff_qs.id,
            order_status = food_order_qs.status, pickup_time_at = today
        )

        food_order_qs.status = 'PICKED'
        food_order_qs.save()

        food_order_qs.ordered_items.update(status="PICKED")
        # For Invoice Generate

        invoice_qs = self.invoice_generator(
            food_order_qs, payment_status="UNPAID")

        serializer = FoodOrderDetailSerializer(instance=food_order_qs)
        return ResponseWrapper(data=serializer.data, status=200)

    def food_order_on_the_way(self, request, *args, **kwargs):
        today = timezone.now()

        order_id = request.data.get('order_id')

        food_order_qs = FoodOrder.objects.filter(id = order_id,
                                                 status__in=['PICKED']).last()

        if not food_order_qs:
            return ResponseWrapper(error_msg='Food Order Not Found',
                                   status=400)

        food_order_log_qs = FoodOrderLog.objects.filter(order_id = order_id).last()

        if food_order_log_qs:
            food_order_log_qs.on_the_way_time_at = today
            food_order_log_qs.order_status = food_order_qs.status
            food_order_log_qs.save()

        food_order_qs.status = 'ON_THE_WAY'
        food_order_qs.save()

        food_order_qs.ordered_items.update(status="ON_THE_WAY")

        serializer = FoodOrderDetailSerializer(instance=food_order_qs)
        return ResponseWrapper(data=serializer.data, status=200)

    def food_order_delivered(self, request, *args, **kwargs):
        today = timezone.now()
        order_id = request.data.get('order_id')

        food_order_qs = FoodOrder.objects.filter(id = order_id,
                                                 status__in = ['ON_THE_WAY']).last()

        if not food_order_qs:
            return ResponseWrapper(error_msg='Food Order Not Found',
                                   status=400)

        food_order_log_qs = FoodOrderLog.objects.filter(order__order_no = food_order_qs.order_no).last()

        if food_order_log_qs:
            food_order_log_qs.delivered_time_at = today
            total_time_duration = today - food_order_log_qs.pickup_time_at

            # .....***..... For Get Total Time Duration Start .....***.....

            total_time = total_time_duration.total_seconds() % (24 * 3600)

            sec = total_time % (24 * 3600)
            hour = int(sec // 3600)
            sec %= 3600
            minutes = int(sec // 60)
            seconds = int(sec % 60)

            # .....***..... For Get Total Time Duration END .....***.....

            food_order_log_qs.total_time = str(hour) + ':' + str(minutes) + ':' + str(seconds)
            food_order_log_qs.save()

        food_order_qs.status = 'DELIVERED'

        # .....***..... START Total Point Add in Customer Profile .....***.....

        total_payable_amount = food_order_qs.payable_amount

        total_point = float(total_payable_amount/100)

        customer_info_qs = food_order_qs.customer
        customer_info_qs.total_point = customer_info_qs.total_point + round(total_point,2)
        customer_info_qs.save()

        # .....***..... END Total Point Add in Customer Profile .....***.....

        food_order_qs.save()

        food_order_qs.ordered_items.update(status="DELIVERED")

        invoice_qs = Invoice.objects.filter(order_id = food_order_qs.id).last()

        if invoice_qs:
            if invoice_qs.payment_status == 'UNPAID':
                invoice_qs.payment_status = 'PAID'
                invoice_qs.save()

        serializer = FoodOrderDetailSerializer(instance=food_order_qs)
        return ResponseWrapper(data=serializer.data, status=200)

    def order_item_cancel(self, request, *args, **kwargs):
        order_item_id = request.data.get('order_item_id')
        order_item_qs = OrderedItem.objects.filter(id=order_item_id).last()
        if order_item_qs:
            order_item_qs.status = 'CANCELLED'
            order_item_qs.save()

            serializer = FoodOrderDetailSerializer(instance=order_item_qs.food_order)
            return ResponseWrapper(data=serializer.data, status=200)
        return ResponseWrapper(error_msg='Order Item Not Found',status=400)

    def all_order_running_order_list(self, request, *args, **kwargs):
        qs = FoodOrder.objects.all().exclude(
            status__in = ['DELIVERED','CANCELLED', 'INVOICE']).order_by('id')
        if not qs:
            return ResponseWrapper(error_msg='No Order is Running Now',
                                   status=400)
        serializer = FoodOrderDetailSerializer(instance=qs, many=True)
        return ResponseWrapper(data=serializer.data, status=200)

    def customer_order_history_list(self, request, *args, **kwargs):
        qs = FoodOrder.objects.filter(customer__user=self.request.user,
                                      invoices__payment_status = 'PAID')

        if not qs:
            return ResponseWrapper(error_msg='Food Order List Not Found', status=400)
        serializer = FoodOrderDetailSerializer(instance=qs, many=True)
        return ResponseWrapper(data=serializer.data, status=200)

    def food_reorder_create(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        order_qs = FoodOrder.objects.all().last()
        food_order_qs = FoodOrder.objects.filter(id=order_id, customer__user=self.request.user, invoices__payment_status = 'PAID').last()

        if not food_order_qs:
            return ResponseWrapper(error_msg='Food Order Not Found',
                                   status=400)

        random_num = random.randint(348, 965)
        today = timezone.now()

        order_no = '#AC' + str(random_num) + str(order_qs.id + 1)

        qs = FoodOrder.objects.create(
            remarks=food_order_qs.remarks, cafe_id=food_order_qs.cafe.id,
            status='ORDER_PLACED', order_no=order_no, customer=food_order_qs.customer,
        )

        for order_item in food_order_qs.ordered_items.all():

            quantity = order_item.quantity
            food_option = order_item.food_option
            food_option_qs = FoodOption.objects.filter(id=food_option.id).last()
            if not food_option_qs:
                return ResponseWrapper(error_msg='Food Option Not Found',
                                       status=400)

            order_item_qs = OrderedItem.objects.create(
                quantity=quantity, food_option_id = food_option_qs.id,
                status = 'ORDER_PLACED', food_order_id = qs.id
            )

            for food_extra in order_item.food_extra.all():
                food_extra_qs = FoodExtra.objects.filter(id=food_extra.id).last()
                order_item_qs.food_extra.add(food_extra_qs.id)

        serializer = FoodOrderDetailSerializer(instance=food_order_qs)
        return ResponseWrapper(data=serializer.data, status=200)


# ............***............ Food Order............***............


class ReportViewSet(CustomViewSet):
    # serializer_class = pass
    queryset = FoodOrder.objects.all()
    lookup_field = 'pk'

    # def get_permissions(self):
    #     permission_classes = []
    #     if self.action in ["all_report"]:
    #         permission_classes = [permissions.IsAdminUser]
    #
    #     else:
    #         permission_classes = [permissions.AllowAny]
    #     return [permission() for permission in permission_classes]

    def all_report(self, request, *args, **kwargs):
        today = timezone.datetime.now()
        this_month = timezone.now().date().replace(day=1)

        week = 7

        weekly_day_wise_income_list = list()

        last_month = (this_month - timedelta(days=1)).replace(day=1)
        this_week_total_sell = 0.0

        this_month_total_sell_list = []

        # Today Total Sell

        today_invoice_qs = Invoice.objects.filter(
            created_at__year=timezone.now().year, created_at__day=timezone.now().day,
            payment_status='PAID')

        total_sell_today = sum(today_invoice_qs.values_list('payable_amount', flat=True))

        # Running week Total Sell

        for day in range(week):

            day_int = (today.weekday() + 1) % 7
            start_of_week = today - timezone.timedelta(day_int-day)

            invoice_qs = Invoice.objects.filter(
                created_at__contains=start_of_week.date(), payment_status='PAID')
            total_list = invoice_qs.values_list('payable_amount', flat=True)

            this_day_total = round(sum(total_list), 2)
            this_week_total_sell += this_day_total

        # Running Month Total Sell

        this_month_invoice_qs = Invoice.objects.filter(
            created_at__year=timezone.now().year, created_at__month=timezone.now().month,
            payment_status='PAID')

        total_sell_this_month = sum(this_month_invoice_qs.values_list('payable_amount', flat=True))

        # Running Month Total Sell

        last_month_invoice_qs = Invoice.objects.filter(
            created_at__year=last_month.year, created_at__month=last_month.month,
            payment_status='PAID')

        total_sell_last_month = sum(last_month_invoice_qs.values_list('payable_amount', flat=True))

        # Total Cloud Cafe

        cloud_cafe_qs = Cafe.objects.all()

        # Total Complete Order

        total_complete_order_qs = Invoice.objects.filter(
            payment_status = 'PAID'
        ).count()

        # Total Staff

        total_manager = CafeStaffInformation.objects.filter(
            is_manager = True
        ).count()

        total_barista = CafeStaffInformation.objects.filter(
            is_barista = True
        ).count()

        total_delivery_boy = CafeStaffInformation.objects.filter(
            is_delivery_boy = True
        ).count()

        for cafe in cloud_cafe_qs:
            invoice_qs = Invoice.objects.filter(
                created_at__year=timezone.now().year, created_at__month=timezone.now().month,
                payment_status='PAID', cafe_id = cafe
            )

            total_sell = sum(invoice_qs.values_list('payable_amount', flat=True))

            this_month_total_sell_list.append({'cafe_id':cafe.id,
                                               'cafe_name':cafe.name,
                                               'total_sell': total_sell})
            # this_month_total_sell_list.append({'page_image':cafe})
            print(this_month_total_sell_list)

        return ResponseWrapper(
            data =
            {
                'total_sell_today': round(total_sell_today, 2),
                'this_week_total_sell': round(this_week_total_sell, 2),
                'total_sell_this_month': round(total_sell_this_month, 2),
                'total_sell_last_month': round(total_sell_last_month, 2),
                'total_cloud_cafe_qs': round(cloud_cafe_qs.count()),
                'total_complete_order_qs': round(total_complete_order_qs),
                'total_manager': round(total_manager),
                'total_barista': round(total_barista),
                'total_delivery_boy': round(total_delivery_boy),
                'this_month_total_sell_list': this_month_total_sell_list,
            },
            msg="success", 
        )

    def dashboard_all_report(self, request, cafe_id, *args, **kwargs):
        cafe_qs = Cafe.objects.filter(id = cafe_id).last()

        if not cafe_qs:
            return ResponseWrapper(error_msg='Cafe Not Found', status=400)

        today = timezone.datetime.now()
        this_month = timezone.now().date().replace(day=1)

        last_month = (this_month - timedelta(days=1)).replace(day=1)
        week = 7

        weekly_day_wise_income_list = list()
        this_week_total_sell = 0.0

        for day in range(week):

            day_int = (today.weekday() + 1) % 7
            start_of_week = today - timezone.timedelta(day_int-day)

            invoice_qs = Invoice.objects.filter(
                created_at__contains=start_of_week.date(), payment_status='PAID',
                cafe_id = cafe_id)
            total_list = invoice_qs.values_list('payable_amount', flat=True)

            this_day_total_order = Invoice.objects.filter(
                created_at__contains=start_of_week.date(),
                payment_status='PAID', cafe_id  = cafe_id).count()

            this_day_total = round(sum(total_list), 2)
            this_week_total_sell += this_day_total
            weekly_day_wise_income_list.append(this_day_total)

        today_invoice_qs = Invoice.objects.filter(
            created_at__year=timezone.now().year, created_at__day=timezone.now().day,
            payment_status='PAID', cafe_id  = cafe_id)

        total_sell_today = sum(today_invoice_qs.values_list('payable_amount', flat =True))

        this_month_invoice_qs = Invoice.objects.filter(
            created_at__year=timezone.now().year, created_at__month=timezone.now().month,
            payment_status='PAID', cafe_id  = cafe_id)

        total_sell_this_month = sum(this_month_invoice_qs.values_list('payable_amount', flat =True))

        this_month_order_qs = Invoice.objects.filter(
            created_at__year=timezone.now().year, created_at__month=timezone.now().month,
            payment_status='PAID', cafe_id  = cafe_id).count()

        last_month_invoice_qs = Invoice.objects.filter(
            created_at__year=last_month.year, created_at__month=last_month.month,
            payment_status='PAID',
            cafe_id  = cafe_id)

        total_sell_last_month = sum(last_month_invoice_qs.values_list('payable_amount', flat =True))

        last_month_total_order = Invoice.objects.filter(
            created_at__year=last_month.year, created_at__month=last_month.month,
            payment_status='PAID',
            cafe_id = cafe_id).count()

        total_running_order_list = FoodOrder.objects.filter(
            status__in = ['ORDER_PLACED','PREPARING','PICKED']
        ).count()

        return ResponseWrapper(
            data=
            {
                'total_sell_today': round(total_sell_today, 2),
                'this_week_total_sell': round(this_week_total_sell, 2),
                'current_month_total_sell': round(total_sell_this_month, 2),
                'current_month_total_order': this_month_order_qs,
                'last_month_total_sell': round(total_sell_last_month, 2),
                'last_month_total_order': last_month_total_order,
                'day_wise_income': weekly_day_wise_income_list,
                'total_running_order_list': total_running_order_list,
            },

            msg="success",
        )

# ............***............ Food Order............***............


class InvoiceViewSet(CustomViewSet):
    serializer_class = FoodOrderDetailSerializer
    queryset = Invoice.objects.all()
    lookup_field = 'pk'

    # def get_permissions(self):
    #     permission_classes = []
    #     if self.action in ["all_complete_order_list"]:
    #         permission_classes = [permissions.IsAdminUser]
    #     else:
    #         permission_classes = [permissions.AllowAny]
    #     return [permission() for permission in permission_classes]    

    def all_complete_order_list(self, request, *args, **kwargs):
        # qs = FoodOrder.objects.filter(invoices__payment_status = 'PAID').order_by('id')
        qs = FoodOrder.objects.filter(status = 'DELIVERED').order_by('id')
        if not qs:
            return ResponseWrapper(error_msg='No Order is Complete Now', status=400)   
        serializer = FoodOrderDetailSerializer(instance=qs, many=True)
        return ResponseWrapper(data=serializer.data, status=200) 


# ............***............ WishList ............***............


class WishListViewSet(CustomViewSet):
    serializer_class = WishListCreateSerializer
    queryset = WishList.objects.all()
    lookup_field = 'pk'
    
    # def get_serializer_class(self):
    #     if self.action in ['category_wise_food_list']:
    #         self.serializer_class = FoodDetailSerializer  
    #     return self.serializer_class

    def get_permissions(self):
        permission_classes = []
        if self.action in ["wish_list_create", 'customer_wish_list', 'wish_list_remove']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def wish_list_create(self, request, *args, **kwargs):
        food_id = request.data.get('food_id')
        food_qs = Food.objects.filter(id=food_id).last()

        if not food_qs:
            return ResponseWrapper(error_msg='Food Not Found',
                                   status=400)

        customer_info = CustomerInfo.objects.filter(user=self.request.user).last()

        if not customer_info:
            return ResponseWrapper(error_msg='You are not a Customer', error_code=400)


        qs = WishList.objects.filter(food=food_qs, customer_id=customer_info.pk)

        if qs:
            return ResponseWrapper(error_msg='Food is Already Add in Wish List',
                                   status=400)

        qs = WishList.objects.create(food=food_qs, customer_id=customer_info.pk)

        serializer = WishListSerializer(instance=qs)

        return ResponseWrapper(data=serializer.data, status=200)

    def customer_wish_list(self, request, *args, **kwargs):
        customer_info = CustomerInfo.objects.filter(user=self.request.user).last()

        qs = WishList.objects.filter(customer_id=customer_info.id)

        serializer = WishListSerializer(instance=qs, many=True)

        return ResponseWrapper(data=serializer.data, status=200)

    def wish_list_remove(self, request, id, *args, **kwargs):
        customer_info = CustomerInfo.objects.filter(user=self.request.user).last()

        qs = WishList.objects.filter(id=id, customer_id = customer_info.pk).last()

        if not qs:
            return ResponseWrapper(error_code=400, error_msg='Favourite Food Not Found')

        qs.delete()

        return ResponseWrapper(msg="WishList Removed", status=200)


    # check commit