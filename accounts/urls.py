from django.urls import path, include
from .views import *

urlpatterns = [
    path('customer_register/',
         LoginViewSet.as_view({'post': 'customer_register'}, name='customer_register')),

    path('customer_register_with_social_media/',
         LoginViewSet.as_view({'post': 'customer_register_with_social_media'},
                              name='customer_register_with_social_media')),
    path('customer_login/',
         LoginViewSet.as_view({'post': 'customer_login'}, name='customer_login')),

    path('check_email/<email>/',
         LoginViewSet.as_view({'get': 'check_email'}, name='check_email')),

    path('check_phone/<phone>/',
         LoginViewSet.as_view({'get': 'check_phone'}, name='check_phone')),

    path('update_password/', LoginViewSet.as_view({'patch':'update_password'}, name='update_password')),

    path('customer_login_with_social_media/',
         LoginViewSet.as_view({'post': 'customer_login_with_social_media'}, name='customer_login_with_social_media')),
    path('login/',
         LoginViewSet.as_view({'post': 'login'}, name='login')),

    path('customer_info_update/',
         LoginViewSet.as_view({'post': 'customer_info_update'},
                              name='customer_info_update')),

    path('customer_details/',
         LoginViewSet.as_view({'get': 'customer_details'},
                              name='customer_details')),

    path('employee_details/',
         LoginViewSet.as_view({'get': 'employee_details'},
                              name='employee_details')),
    
    # ....................***.......Delivery Boy..........***..............................
    
    path('delivery_boy_list/<cafe_id>/',
         CafeStaffInformationViewSet.as_view({'get': 'delivery_boy_list'},
                              name='delivery_boy_list')),

    path('staff_information_details/<staff_id>/',
         CafeStaffInformationViewSet.as_view({'get': 'staff_information_details'},
                                             name="staff_information_details")),

    path('all_staff_list/<cafe_id>/',
         CafeStaffInformationViewSet.as_view({'get': 'all_staff_list'},
                              name='all_staff_list')),
    path('create_manager/',
         CafeStaffInformationViewSet.as_view({'post': 'create_manager'},
                                             name='create_manager')),
    
    path('create_barista/',
         CafeStaffInformationViewSet.as_view({'post': 'create_barista'},
                                             name='create_barista')),
    
    path('create_delivery_boy/',
         CafeStaffInformationViewSet.as_view({'post': 'create_delivery_boy'},
                                             name='create_delivery_boy')),
    
    path('create_staff/',
         CafeStaffInformationViewSet.as_view({'post': 'create_staff'},
                                             name='create_staff')),
    
    path('update_manager/<pk>/', CafeStaffInformationViewSet.as_view(
        {'patch': 'update_manager'}),
         name="update_manager"),
    
    path('update_barista/<pk>/', CafeStaffInformationViewSet.as_view(
        {'patch': 'update_barista'}),
         name="update_barista"),
    
    path('update_delivery_boy/<pk>/', CafeStaffInformationViewSet.as_view(
        {'patch': 'update_delivery_boy'}),
         name="update_delivery_boy"),
    
    path('update_staff/<pk>/', CafeStaffInformationViewSet.as_view(
        {'patch': 'update_staff'}),
         name="update_staff"),
    
    path('manager_list/<cafe_id>/',
         CafeStaffInformationViewSet.as_view({'get': 'manager_list'},
                              name='manager_list')),

    path('barista_list/<cafe_id>/',
         CafeStaffInformationViewSet.as_view({'get': 'barista_list'},
                              name='barista_list')),
    
    path('manager_delete/<pk>/', CafeStaffInformationViewSet.as_view(
        {'delete': 'manager_delete'}),
         name="manager_delete"),

    path('manager_details/<pk>/', CafeStaffInformationViewSet.as_view(
        {'get': 'manager_details'}),
         name="manager_details"),

    path('customer_fcm_create/', UserFcmDeviceViewSet.as_view(
        {'post': 'customer_fcm_create'}),
         name="customer_fcm_create"),
]