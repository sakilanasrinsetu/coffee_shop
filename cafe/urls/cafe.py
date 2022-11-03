from django.urls import path
from ..views import *
from cafe import views

cafe_urls = [

    # ..........***.......... CloudCafeInformation Url Start ..........***..........

    path('cloud_cafe_information_details/', CloudCafeInformationViewSet.as_view(
        {'get': 'cloud_cafe_information_details'}),
         name="cloud_cafe_information_details"),

    path('cloud_cafe_information_create/', CloudCafeInformationViewSet.as_view(
        {'post': 'cloud_cafe_information_create'}),
         name="cloud_cafe_information_create"),

    path('cloud_cafe_information_update/<pk>/', CloudCafeInformationViewSet.as_view(
        {'patch': 'cloud_cafe_information_update'}),
         name="cloud_cafe_information_update"),

    # ..........***.......... Cafe Url Start ..........***.............................

    path('cafe_create/', CafeViewSet.as_view(
        {'post': 'cafe_create'}),
         name="cafe_create"),

    path('cafe_update/<pk>/', CafeViewSet.as_view(
        {'patch': 'cafe_update'}),
         name="cafe_update"),

    path('cafe_delete/<pk>/', CafeViewSet.as_view(
        {'delete': 'cafe_delete'}),
         name="cafe_delete"),

    path('cafe_details/<pk>/', CafeViewSet.as_view(
        {'get': 'cafe_details'}),
         name="cafe_details"),

    path('cafe_list/', CafeViewSet.as_view(
        {'get': 'cafe_list'}),
         name="cafe_list"),

    path('cafe_custom_update/<pk>/', CafeViewSet.as_view(
        {'patch': 'cafe_custom_update'}),
         name="cafe_custom_update"),
    
    path('cafe_wise_review_list/<cafe_id>/', ReviewViewSet.as_view(
        {'get': 'cafe_wise_review_list'}),
         name="cafe_wise_review_list"),

    # ..........***.......... Category Url Start ..........***.............................

    path('category_details/<pk>/', CategoryViewSet.as_view(
        {'get': 'category_details'}),
         name="category_details"),

    path('category_list/', CategoryViewSet.as_view(
        {'get': 'category_list'}),
         name="category_list"),

    path('category_create/', CategoryViewSet.as_view(
        {'post': 'category_create'}),
         name="category_create"),

    path('category_update/<pk>/', CategoryViewSet.as_view(
        {'patch': 'category_update'}),
         name="category_update"),

    path('category_delete/<pk>/', CategoryViewSet.as_view(
        {'delete': 'category_delete'}),
         name="category_delete"),
    
    path('category_wise_food_list/<slug>/',
         CategoryViewSet.as_view({'get': 'category_wise_food_list'},
                                 name='category_wise_food_list')),

    # ..........***.......... Notification Url Start ..........***.............................

    path('notification_create/', NotificationViewSet.as_view(
        {'post': 'notification_create'}),
         name="notification_create"),

    path('notification_update/<pk>/', NotificationViewSet.as_view(
        {'patch': 'notification_update'}),
         name="notification_update"),

    path('notification_delete/<pk>/', NotificationViewSet.as_view(
        {'delete': 'notification_delete'}),
         name="notification_delete"),

    path('notification_details/<pk>/', NotificationViewSet.as_view(
        {'get': 'notification_details'}),
         name="notification_details"),

    path('notification_list/', NotificationViewSet.as_view(
        {'get': 'notification_list'}),
         name="notification_list"),
    
   
    # ........***........ Food ........***.............................

    path('food_create/', FoodViewSet.as_view(
        {'post': 'food_create'}),name="food_create"),
    path('food_all_details/<slug>/', FoodViewSet.as_view(
        {'get': 'food_all_details'}),name="food_all_details"),
    path('food_details/<id>/', FoodViewSet.as_view(
        {'get': 'food_details'}),name="food_details"),
    path('food/', FoodViewSet.as_view(
        {'get': 'list'}),name="list"),
    path('available_food_list/', FoodViewSet.as_view(
        {'get': 'available_food_list'}),name="available_food_list"),
    path('food_update/<pk>/', FoodViewSet.as_view(
        {'patch': 'food_update'}),name="food_update"),
    path('all_food_list/<cafe_id>/', FoodViewSet.as_view(
        {'get': 'all_food_list'}),name="all_food_list"),
    
    # ..........***.......... Review Url Start ..........***.............................

    path('review_details/<pk>/', ReviewViewSet.as_view(
        {'get': 'review_details'}),
         name="review_details"),

    path('review_list/', ReviewViewSet.as_view(
        {'get': 'review_list'}),
         name="review_list"),

    path('review_create/', ReviewViewSet.as_view(
        {'post': 'review_create'}),
         name="review_create"),

    path('review_update/<pk>/', ReviewViewSet.as_view(
        {'patch': 'review_update'}),
         name="review_update"),

    path('review_delete/<pk>/', ReviewViewSet.as_view(
        {'delete': 'review_delete'}),
         name="review_delete"),

    path('running_order_list/<cafe_id>/', FoodOrderViewSet.as_view(
        {'get': 'running_order_list'}),
         name="running_order_list"),

    # path('food_order_preparing/', FoodOrderViewSet.as_view(
    #     {'post': 'food_order_preparing'}),
    #      name="food_order_preparing"),
    
    path('total_running_order_list/<cafe_id>/', FoodOrderViewSet.as_view(
        {'get': 'total_running_order_list'}),
         name="total_running_order_list"),

    path('food_order_preparing/', FoodOrderViewSet.as_view(
        {'post': 'food_order_preparing'}),
         name="food_order_preparing"),

    path('food_order_cancel/', FoodOrderViewSet.as_view(
        {'post': 'food_order_cancel'}),
         name="food_order_cancel"),

    # path('food_order_picked/', FoodOrderViewSet.as_view(
    #     {'post': 'food_order_picked'}),
    #      name="food_order_picked"),

    # path('food_order_delivered/', FoodOrderViewSet.as_view(
    #     {'post': 'food_order_delivered'}),
    #      name="food_order_delivered"),
    
    path('order_item_cancel/', FoodOrderViewSet.as_view(
        {'post': 'order_item_cancel'}),
         name="order_item_cancel"),

    path('food_order_picked/', FoodOrderViewSet.as_view(
        {'post': 'food_order_picked'}),
         name="food_order_picked"),

    path('food_order_delivered/', FoodOrderViewSet.as_view(
        {'post': 'food_order_delivered'}),
         name="food_order_delivered"),

    path('dashboard_all_report/<cafe_id>/', ReportViewSet.as_view(
        {'get': 'dashboard_all_report'}),
         name="dashboard_all_report"),

    path('all_report/', ReportViewSet.as_view(
        {'get': 'all_report'}),
         name="all_report"),
    
    path('all_order_running_order_list/', FoodOrderViewSet.as_view(
        {'get': 'all_order_running_order_list'}),
         name="all_order_running_order_list"),
    
    path('all_complete_order_list/', InvoiceViewSet.as_view(
        {'get': 'all_complete_order_list'}),
         name="all_complete_order_list"),
    
]
