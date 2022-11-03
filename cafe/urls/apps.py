from django.urls import path
from ..views import *
from cafe import views

apps_url = [

    # ..........***.......... CloudCafeInformation Url Start ..........***..........

    path('category_wise_food_list/<slug>/',
         CategoryViewSet.as_view({'get': 'category_wise_food_list'},
                                 name='category_wise_food_list')),
    
    path('category_list/', CategoryViewSet.as_view(
        {'get': 'category_list'}), name="category_list"),

    path('food_list/', CategoryViewSet.as_view(
        {'get': 'all_food_list'}), name="all_food_list"),

    path('food_search/<title>/', FoodViewSet.as_view(
        {'get': 'food_search'}), name="food_search"),

    path('recommended_food_list/', FoodViewSet.as_view(
        {'get': 'recommended_food_list'}), name="recommended_food_list"),
    
    path('category_details/<pk>/', CategoryViewSet.as_view(
        {'get': 'category_details'}),
         name="category_details"),
    
    path('category_wise_food_list/<slug>/',
         CategoryViewSet.as_view({'get': 'category_wise_food_list'},
                                 name='category_wise_food_list')),

    path('food_order_create/', FoodOrderViewSet.as_view(
        {'post': 'food_order_create'}),
         name="food_order_create"),

    path('food_order_details/<id>/', FoodOrderViewSet.as_view(
        {'get': 'food_order_details'}),
         name="food_order_details"),
    
    path('food_all_details/<slug>/', FoodViewSet.as_view({
        'get': 'food_all_details'}),
         name="food_all_details"),
    
    path('food_details/<slug>/', FoodViewSet.as_view({
        'get': 'food_details'}),
         name="food_details"),
    
    path('available_food_list/', FoodViewSet.as_view({
        'get': 'available_food_list'}),
         name="available_food_list"),

    path('notification_list/', NotificationViewSet.as_view(
        {'get': 'notification_list'}),
         name="notification_list"),
    
    path('food_order_cancel/', FoodOrderViewSet.as_view(
        {'post': 'food_order_cancel'}),
         name="food_order_cancel"),
    
    path('customer_order_history_list/', FoodOrderViewSet.as_view(
        {'get': 'customer_order_history_list'}),
         name="customer_order_history_list"),

    path('food_reorder_create/', FoodOrderViewSet.as_view(
            {'post': 'food_reorder_create'}),
         name="food_reorder_create"),
    
    path('wish_list_create/', WishListViewSet.as_view(
        {'post': 'wish_list_create'}),
         name="wish_list_create"),

    path('customer_wish_list/', WishListViewSet.as_view(
        {'get': 'customer_wish_list'}),
         name="customer_wish_list"),

    path('wish_list_remove/<id>/', WishListViewSet.as_view(
        {'delete': 'wish_list_remove'}),
         name="wish_list_remove"),

    path('food_order_on_the_way/', FoodOrderViewSet.as_view(
        {'post': 'food_order_on_the_way'}),
         name="food_order_on_the_way"),

    ]