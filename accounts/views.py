from django.shortcuts import render
from requests import request

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken, TokenAuthentication
from .serializers import RegisterSerializer
from utils.custom_viewset import CustomViewSet
from utils.custom_permissions import *
from accounts.models import UserAccount
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions, status, viewsets

from django.utils import timezone
from drf_yasg2.utils import swagger_auto_schema
from django.contrib.auth import get_user_model, login
import random
from accounts.serializers import *
from cafe.serializers import Cafe
from utils.response_wrapper import ResponseWrapper

from django.contrib.auth.hashers import make_password


# Create your views here.

class LoginViewSet(CustomViewSet):
    queryset = Cafe.objects.all()
    lookup_field = 'pk'
    # logging_methods = ['GET', 'POST', 'PATCH', 'DELETE']
    # # serializer_class = CafeContactPerson

    def get_permissions(self):
        permission_classes = []
        if self.action in ["customer_info_update", "customer_details", "employee_details"]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            # permissions.DjangoObjectPermissions.has_permission()
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == ['customer_login']:
            self.serializer_class = AuthTokenSerializer

        elif self.action == ['update_password']:
            self.serializer_class = AuthTokenSerializer

        if self.action == 'customer_info_update':
            self.serializer_class = CustomerInfoUpdateSerializer

        elif self.action == 'customer_login_with_social_media':
            self.serializer_class = SocialAuthTokenSerializer

        elif self.action == 'login':
            self.serializer_class = AuthTokenSerializer

        elif self.action == 'customer_register':
            self.serializer_class = RegisterSerializer

        elif self.action == 'customer_register_with_social_media':
            self.serializer_class = CustomerInfoUpdateWithSocialMediaSerializer

        else:
            self.serializer_class = AuthTokenSerializer

        return self.serializer_class

    def check_email(self, request,email, *args, **kwargs):
        email_exist = UserAccount.objects.filter(email=email).exists()

        if email_exist:
            return ResponseWrapper(msg=True, status=200)

        return ResponseWrapper(msg=False, status=400)

    def check_phone(self, request, phone, *args, **kwargs):
        phone_exist = UserAccount.objects.filter(phone=phone)

        if phone_exist:
            return ResponseWrapper(msg=True, status=200)

        return ResponseWrapper(msg=False, status=400)

    def customer_login(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username:
            return ResponseWrapper(error_msg='User Name is Not Given', status=400)

        customer_qs = CustomerInfo.objects.filter(Q(user__phone=username)| Q(user__email=username)
                                        ).last()

        if not customer_qs:
            return ResponseWrapper(error_msg='Customer Not Found', status=400)

        elif customer_qs.user.check_password(password):
            _, token = AuthToken.objects.create(customer_qs.user)
            serializer = UserDetailsSerializer(instance=customer_qs.user)

            context = {
                'user_info': serializer.data,
                'token': token,
            }
            return ResponseWrapper(data=context, status=200)

        return ResponseWrapper(error_msg="Password Doesn't Match", status=400)

    def update_password(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username:
            return ResponseWrapper(error_msg='User Name is Not Given', status=400)

        user_qs = UserAccount.objects.filter(Q(phone=username)| Q(email=username)
                                        ).last()

        customer_qs = CustomerInfo.objects.filter(Q(user__phone=username)| Q(user__email=username)
                                        ).last()

        if not customer_qs:
            return ResponseWrapper(error_msg='Customer Not Found', status=400)

        password = make_password(password)

        user_qs.password = password
        user_qs.save()

        _, token = AuthToken.objects.create(customer_qs.user)
        serializer = UserDetailsSerializer(instance=customer_qs.user)

        context = {
            'user_info': serializer.data,
            'token': token,
        }
        return ResponseWrapper(data=context, status=200)

        # return ResponseWrapper(error_msg="Password Doesn't Match", status=400)

    def customer_login_with_social_media(self, request, *args, **kwargs):
        username = request.data.get('email')
        customer_qs = CustomerInfo.objects.filter(user__email=username).last()
        if not customer_qs:
            return ResponseWrapper(error_msg='User Not Found', status=400)

        _, token = AuthToken.objects.create(customer_qs.user)
        serializer = UserDetailsSerializer(instance=customer_qs.user)

        context = {
            'user_info': serializer.data,
            'token': token,
        }
        return ResponseWrapper(data=context, status=200)


    def login(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        cafe_staff_qs = CafeStaffInformation.objects.filter(Q(user__phone=username)| Q(user__email=username)
                                        ).last()
        if not cafe_staff_qs:
            super_user_qs = UserAccount.objects.filter(Q(phone=username)
                                                       | Q(email=username),
                                                        is_superuser = True
                                                        ).last()
            if not super_user_qs:
                return ResponseWrapper(error_msg='Username is Not Valid', status=400)

            elif super_user_qs.check_password(password):
                _, token = AuthToken.objects.create(super_user_qs)
                serializer = UserSerializer(instance=super_user_qs)

                context = {
                    'user_info': serializer.data,
                    'token': token,
                }
                return ResponseWrapper(data=context, status=200)

        elif cafe_staff_qs.user.check_password(password):
            _, token = AuthToken.objects.create(cafe_staff_qs.user)
            serializer = CafeStaffInformationSerializer(instance=cafe_staff_qs)

            context = {
                'user_info': serializer.data,
                'token': token,
            }
            return ResponseWrapper(data=context, status=200)

        return ResponseWrapper(error_msg='Password is Not Valid', status=400)

    def customer_register(self, request, *args, **kwargs):
        password = request.data.pop("password")
        email = request.data["email"]
        phone = request.data["phone"]
        verification_id = uuid.uuid4().__str__()

        email_exist = UserAccount.objects.filter(email=email).exists()

        if email_exist:
            return ResponseWrapper(
                error_msg="Email is Already Used", status=400
            )

        phone_exist = UserAccount.objects.filter(phone=phone).exists()

        if phone_exist:
            return ResponseWrapper(
                error_msg="Phone Number is Already Used", status=400
            )
        try:
            password = make_password(password=password)
            user = UserAccount.objects.create(
                # email=email,
                password=password,
                # verification_id=verification_id,
                **request.data
            )
            _, token = AuthToken.objects.create(user)
            # user.email = email
            # user.save()
            customer_qs = CustomerInfo.objects.create(
                email=email, phone=phone, user_id=user.id
            )
        except Exception as err:
            # logger.exception(msg="error while account cration")
            return ResponseWrapper(
                error_msg="Account Can't Create", status=400
            )

        serializer = UserDetailsSerializer(instance=user)

        context = {
            'user_info': serializer.data,
            'token': token,
        }
        return ResponseWrapper(data=context, status=200)

    def customer_info_update(self, request, *args, **kwargs):
        name = request.data.get("name")
        date_of_birthday = request.data.get("date_of_birthday")
        image = request.data.get("image")
        gender = request.data.get("gender")

        if not date_of_birthday:
            return ResponseWrapper(error_msg='Date of Birth is not Given',
                                   error_code=400)
        if not gender:
            return ResponseWrapper(error_msg='Gender is not Given',
                                   error_code=400)

        qs = CustomerInfo.objects.filter(user=self.request.user).last()

        if not qs:
            return ResponseWrapper(error_msg='This is Not Your Account',
                                   error_code=400)

        qs.name = name
        qs.date_of_birthday = date_of_birthday
        if image:
            qs.image = image
        qs.gender = gender
        qs.save()

        serializer = CustomerInfoSerializer(instance=qs)

        context = {
            'user_info': {
                'id': qs.user.id,
                'email': qs.email,
                'customer_info' : serializer.data
            },
            'token': None,
        }

        return ResponseWrapper(data=context, status=200)

    def customer_details(self, request, *args, **kwargs):
        qs = CustomerInfo.objects.filter(user=self.request.user).last()

        if not qs:
            return ResponseWrapper(error_msg='This is Not Your Account',
                                   error_code=400)

        serializer = CustomerInfoSerializer(instance=qs)

        context = {
            'user_info': {
                'id': qs.user.id,
                'email': qs.email,
                'customer_info' : serializer.data
            },
            'token': None,
        }

        return ResponseWrapper(data=context, status=200)


    def employee_details(self, request, *args, **kwargs):
        qs = CafeStaffInformation.objects.filter(user=self.request.user).last()

        if not qs:
            return ResponseWrapper(error_msg='This is Not Your Account',
                                   error_code=400)
        serializer = CafeStaffInformationSerializer(instance=qs)

        _, token = AuthToken.objects.create(qs.user)

        context = {
            'user_info': serializer.data,
            'token': token,
        }
        return ResponseWrapper(data=context, status=200)

    def customer_register_with_social_media(self, request, *args, **kwargs):
        name = request.data.get("name")
        email = request.data.get("email")
        phone = request.data.get("phone")
        date_of_birthday = request.data.get("date_of_birthday")
        image = request.data.get("image")
        gender = request.data.get("gender")

        user_email_qs = CustomerInfo.objects.filter(email=email).last()

        if user_email_qs:
            return ResponseWrapper(error_msg='Email Already Found',
                                   error_code=400)

        user_phone_qs = CustomerInfo.objects.filter(phone=phone).last()

        if user_phone_qs:
            return ResponseWrapper(error_msg='Phone Already Found',
                                   error_code=400)

        random_num = random.randint(14598, 963415)

        user = UserAccount.objects.create(
            email = email, phone = phone, password = random_num
        )
        qs = CustomerInfo.objects.create(
            name=name, image=image, email=email, phone=phone,
            date_of_birthday=date_of_birthday, gender=gender, user = user
        )
        _, token = AuthToken.objects.create(user)

        serializer = CustomerInfoSerializer(instance=qs)
        context = {
            'user_info': {
                'id': qs.user.id,
                'email': qs.email,
                'customer_info': serializer.data
            },
            'token': token,
        }
        return ResponseWrapper(data=context, status=200)


class CafeStaffInformationViewSet(CustomViewSet):
    queryset = CafeStaffInformation.objects.all()
    lookup_field = 'pk'
    serializer_class = CafeStaffInformationSerializer

    # ..........***..........Devevery Boy List ..........***..........
    
    # def get_permissions(self):
    #     permission_classes = []
    #     if self.action in ["create_manager", "create_barista", "create_delivery_boy",
    #                        "create_staff", "update_manager", "update_barista",
    #                        "update_delivery_boy", "update_staff", "delivery_boy_delete",
    #                        "barista_delete", "staff_delete", "manager_delete", "manager_details",
    #                        "barista_details","delivery_boy_details", "staff_details"]:
    #         permission_classes = [permissions.IsAdminUser]
    #     else:
    #         # permissions.DjangoObjectPermissions.has_permission()
    #         permission_classes = [permissions.AllowAny]
    #     return [permission() for permission in permission_classes]


    def get_serializer_class(self):
        if self.action == ['create_staff', 'create_manager']:
            self.serializer_class = EmployeeCreateSerializer
        elif self.action == ['create_barista', 'update_barista']:
            self.serializer_class = EmployeeCreateSerializer 
        elif self.action == ['create_delivery_boy', 'update_delivery_boy']:
            self.serializer_class = EmployeeCreateSerializer 
        elif self.action == ['update_staff']:
            self.serializer_class = EmployeeCreateSerializer  
        else:
            self.serializer_class = EmployeeCreateSerializer        
        return self.serializer_class

    def delivery_boy_list(self, request, cafe_id, *kwargs, **args):
        qs = CafeStaffInformation.objects.filter(cafe_id = cafe_id, is_delivery_boy= True)
        # if not qs:
        #     return ResponseWrapper(error_code=400, error_msg='Failed')
        serializer = CafeStaffInformationSerializer(instance=qs, many=True)
        return ResponseWrapper(data=serializer.data, status=200)

    def staff_information_details(self, request, staff_id, *kwargs, **args):
        qs = CafeStaffInformation.objects.filter(pk = staff_id).last()

        if not qs:
            return ResponseWrapper(error_code=400, error_msg="staff not found")

        serializer = CafeStaffInformationSerializer(instance = qs)
        return ResponseWrapper(data=serializer.data, status=200)

    def all_staff_list(self, request, cafe_id, *kwargs, **args):
        staff_list = []
        qs = CafeStaffInformation.objects.filter(cafe_id = cafe_id)
        if not qs:
            return ResponseWrapper(error_code=400, error_msg='Failed')
        delivery_boy_list_qs = qs.filter(is_delivery_boy = True)
        delivery_boy_list = CafeStaffInformationSerializer(instance=delivery_boy_list_qs,
                                                           many=True)
        manager_list_qs = qs.filter(is_manager = True)
        manager_list = CafeStaffInformationSerializer(instance=manager_list_qs,
                                                           many=True)
        barista_qs = qs.filter(is_barista = True)
        barista_list = CafeStaffInformationSerializer(instance=barista_qs,
                                                           many=True)

        # staff_list.append({'delivery_boy_list':delivery_boy_list.data})
        # staff_list.append({'manager_list':manager_list.data})
        # staff_list.append({'barista_list':barista_list.data})
        return ResponseWrapper(data={
            # 'staff_list':staff_list
            'manager_list':manager_list.data,
            'delivery_boy_list':delivery_boy_list.data,
            'barista_list':barista_list.data,
        }, status=200)

    def create_manager(self, request, *args, **kwargs):
        return self.create_employee(request, is_manager=True)

    # ..........***.......... Manager Update ..........***..........
    
    def update_manager(self, request, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            qs = serializer.update(instance=self.get_object(
            ), validated_data=serializer.validated_data)
            serializer = self.serializer_class(instance=qs)
            return ResponseWrapper(data=serializer.data)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
   
   
    # ..........***..........Manager List ..........***..........

        # password = request.data.pop("password")
        # employee_id = request.data.get("staff_id")
        # name = request.data.get("name")
        # cafe = request.data.get("cafe")
        # phone = request.data.get("phone")
        # date_of_birth = request.data.get("date_of_birth")
        # email = request.data.get("email")
        # nid = request.data.get("nid")
        # shift_start_hour = request.data.get("shift_start_hour")
        # shift_end_hour = request.data.get("shift_end_hour")
        # is_active = request.data.get("is_active")
        #
        # email_exist = UserAccount.objects.filter(email=email).exists()
        #
        # if email_exist:
        #     return ResponseWrapper(
        #         data="Please use different Email, "
        #              "it’s already been in use",
        #         status=400
        #     )
        #
        # cafe_qs = Cafe.objects.filter(id = cafe).last()
        # if not cafe_qs:
        #     return ResponseWrapper(error_code=400, error_msg='Cafe Not Found')
        #
        # qs = CafeStaffInformation.objects.create(
        #     staff_id = employee_id, name = name,cafe_id = cafe_qs.pk,
        #     phone = phone, email = email, date_of_birth = date_of_birth, shift_start_hour = shift_start_hour,
        #     shift_end_hour = shift_end_hour, is_active = is_active, is_manager = True
        # )
        #
        # try:
        #     password = make_password(password=password)
        #     user = UserAccount.objects.create(
        #         # email=email,
        #         password=password,
        #         # verification_id=verification_id,
        #         **request.data
        #     )
        #     customer_qs = CustomerInfo.objects.create(
        #         email=email, phone=phone, user_id=user.id
        #     )
        # except Exception as err:
        #     # logger.exception(msg="error while account creation")
        #     return ResponseWrapper(
        #         data="Account creation failed", status=401
        #     )
        #
        # serializer = CafeStaffInformationSerializer(instance=qs)
        # return ResponseWrapper(data=serializer.data, status=200)
        return self.create_employee(request, is_manager=True)

    def manager_list(self, request, cafe_id, *kwargs, **args):
        qs = CafeStaffInformation.objects.filter(cafe_id=cafe_id, is_manager= True)
        # if not qs:
        #     return ResponseWrapper(error_code=400, error_msg='Failed')
        serializer = CafeStaffInformationSerializer(instance=qs, many=True)
        return ResponseWrapper(data=serializer.data, status=200)

    # ..........***..........Manager Delete ..........***..........

    def manager_delete(self, request, **kwargs):
        qs = self.queryset.filter(**kwargs).first()
        if qs:
            qs.delete()
            return ResponseWrapper(status=200, msg='deleted')
        else:
            return ResponseWrapper(error_msg="failed to delete", error_code=400)

    # ..........***.......... Manager Details ..........***..........

    def manager_details(self, request, *args, **kwargs):
        staff_details_qs = CafeStaffInformation.objects.all().last()
        if not staff_details_qs:
            return ResponseWrapper(error_msg='Manager Details Not Found', status=400)
        serializer = CafeStaffInformationSerializer(instance=staff_details_qs)
        return ResponseWrapper(data=serializer.data, status=200)     

   # ..........***..........Devevery Boy List ..........***..........

    # def delivery_boy_list(self, request, cafe_id, *kwargs, **args):
    #     qs = CafeStaffInformation.objects.filter(cafe_id=cafe_id)
    #     if not qs:
    #         return ResponseWrapper(error_code=400, error_msg='Failed')
    #     serializer = CafeStaffInformationSerializer(instance=qs, many=True)
    #     return ResponseWrapper(data=serializer.data, status=200)

    # ..........***.......... Delivery Boy Create ..........***..........
    
    def create_delivery_boy(self, request, *kwargs, **args):
        return self.create_employee(request, is_manager=True)

    # ..........***.......... Delivery Boy Update ..........***..........

    def update_delivery_boy(self, request, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            qs = serializer.update(instance=self.get_object(
            ), validated_data=serializer.validated_data)
            serializer = self.serializer_class(instance=qs)
            return ResponseWrapper(data=serializer.data)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
    
    # ..........***..........Delevery Boy Delete ..........***..........

    def delivery_boy_delete(self, request, **kwargs):
        qs = self.queryset.filter(**kwargs).first()
        if qs:
            qs.delete()
            return ResponseWrapper(status=200, msg='deleted')
        else:
            return ResponseWrapper(error_msg="failed to delete", error_code=400)

    # ..........***.......... Devevery Boy Details ..........***..........

    def delivery_boy_details(self, request, *args, **kwargs):
        delivery_boy_details_qs = CafeStaffInformation.objects.all().last()
        if not delivery_boy_details_qs:
            return ResponseWrapper(error_msg='Devevery Boy Details Not Found', status=400)
        serializer = CafeStaffInformationSerializer(instance=delivery_boy_details_qs)
        return ResponseWrapper(data=serializer.data, status=200)   
    
    
    # ..........***..........Barista List ..........***..........


    def barista_list(self, request, cafe_id, *kwargs, **args):
        qs = CafeStaffInformation.objects.filter(cafe_id=cafe_id, is_barista = True)
        # if not qs:
        #     return ResponseWrapper(error_code=400, error_msg='Failed')
        serializer = CafeStaffInformationSerializer(instance=qs, many=True)
        return ResponseWrapper(data=serializer.data, status=200)
    
    # ..........***.......... Barista Create ..........***..........

    def create_barista(self, request, *kwargs, **args):
        return self.create_employee(request, is_manager=True)
    
    
    # ..........***.......... Barista Update ..........***..........
    
    
    def update_barista(self, request, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            qs = serializer.update(instance=self.get_object(
            ), validated_data=serializer.validated_data)
            serializer = self.serializer_class(instance=qs)
            return ResponseWrapper(data=serializer.data)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
    
    # ..........***..........Barista Delete ..........***..........
    
    
    def barista_delete(self, request, **kwargs):
        qs = self.queryset.filter(**kwargs).first()
        if qs:
            qs.delete()
            return ResponseWrapper(status=200, msg='deleted')
        else:
            return ResponseWrapper(error_msg="failed to delete", error_code=400)
        
    
    # ..........***.......... Barista Details ..........***..........


    def barista_details(self, request, *args, **kwargs):
        barista_details_qs = CafeStaffInformation.objects.all().last()
        if not barista_details_qs:
            return ResponseWrapper(error_msg='Barista Details Not Found', status=400)
        serializer = CafeStaffInformationSerializer(instance=barista_details_qs)
        return ResponseWrapper(data=serializer.data, status=200)  
    
    
    # ..........***..........Staff List ..........***..........


    def staff_list(self, request, cafe_id, *kwargs, **args):
        qs = CafeStaffInformation.objects.filter(cafe_id=cafe_id)
        if not qs:
            return ResponseWrapper(error_code=400, error_msg='Failed')
        serializer = CafeStaffInformationSerializer(instance=qs, many=True)
        return ResponseWrapper(data=serializer.data, status=200)

    # ..........***.......... Staff Create ..........***..........

    def create_staff(self, request, *kwargs, **args):
        return self.create_employee(request, is_staff=True)

    # ..........***.......... Staff Update ..........***..........
    
    def update_staff(self, request, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            qs = serializer.update(instance=self.get_object(
            ), validated_data=serializer.validated_data)
            serializer = self.serializer_class(instance=qs)
            return ResponseWrapper(data=serializer.data)
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)
               
    
    # ..........***..........Staff Delete ..........***..........
    
    
    def staff_delete(self, request, **kwargs):
        qs = self.queryset.filter(**kwargs).first()
        if qs:
            qs.delete()
            return ResponseWrapper(status=200, msg='deleted')
        else:
            return ResponseWrapper(error_msg="failed to delete", error_code=400)
        
    
    # ..........***.......... Staff Details ..........***..........


    def staff_details(self, request, *args, **kwargs):
        staff_details_qs = CafeStaffInformation.objects.all().last()
        if not staff_details_qs:
            return ResponseWrapper(error_msg='Staff Details Not Found', status=400)
        serializer = CafeStaffInformationSerializer(instance=staff_details_qs)
        return ResponseWrapper(data=serializer.data, status=200)

    def create_employee(self, request, is_barista=False, is_manager=False, is_delivery_boy = False,
                     is_staff = False):
        password=request.data.pop("password")
        staff_id = request.data.get('staff_id')

        name = request.data.get('name')
        cafe_id = request.data.get('cafe_id')
        phone = request.data.get("phone")
        email = request.data.get("email")
        date_of_birth = request.data.get("date_of_birth")
        nid = request.data.get("nid")
        shift_start_hour = request.data.get("shift_start_hour")
        shift_end_hour = request.data.get("shift_end_hour")
        is_active = request.data.get("is_active")

        cafe_qs = Cafe.objects.filter(id=cafe_id).last()
        email_exist = UserAccount.objects.filter(email=email).exists()

        if email_exist:
            return ResponseWrapper(
                data="Please use different Email, it’s already been in use", status=400
            )

        phone_exist = UserAccount.objects.filter(phone=phone).exists()

        if phone_exist:
            return ResponseWrapper(
                data="Please use different Phone, it’s already been in use", status=400
            )

        try:
            password = make_password(password=password)
            user = UserAccount.objects.create(
                phone=phone,
                email=email,
                password=password,
            )

            staff_qs = CafeStaffInformation.objects.create(
                staff_id=staff_id, name=name,
                email=email, phone=phone, cafe_id=cafe_qs.id,
                date_of_birth=date_of_birth, nid=nid,
                shift_end_hour=shift_end_hour,
                shift_start_hour=shift_start_hour,
                is_active=is_active, user=user,
                is_manager = is_manager, is_barista = is_barista,
                is_delivery_boy = is_delivery_boy, is_staff = is_staff
            )
            serializer = CafeStaffInformationSerializer(instance=staff_qs)

            return ResponseWrapper(data=serializer.data, status=200)

        except Exception as err:
            return ResponseWrapper(
                error_msg="Account Can't Create", status=400
            )


class UserFcmDeviceViewSet(CustomViewSet):
    queryset = CustomerFcmDevice.objects.all()
    lookup_field = 'customer'
    serializer_class = CustomerFcmDeviceSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def customer_fcm_create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            customer_fcm_qs = CustomerFcmDevice.objects.filter(
                customer_id=request.data.get("customer"))
            customer_fcm_qs.delete()
            qs = serializer.save()
            serializer = self.serializer_class(instance=qs)
            return ResponseWrapper(data=serializer.data, msg='created')
        else:
            return ResponseWrapper(error_msg=serializer.errors, error_code=400)