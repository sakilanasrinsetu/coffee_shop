from dataclasses import field, fields
from .models import *
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField, Base64FileField
from django.utils.html import strip_tags
# from utils.calculate_price import calculate_price
import datetime
from django.utils import timezone
from datetime import datetime
from accounts.models import CustomerInfo
from django.db.models import Q
from utils.calculate_price import *
from dataclasses import field
from rest_framework import serializers, validators


BASE_URL = 'http://127.0.0.1:8000/media/'


# ..........***.......... Customer Info Start ..........***..........

class CustomerInfoSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomerInfo
        fields = '__all__'

    def get_image_url(self, obj):
        if obj.image:
            file_name = obj.image
            return BASE_URL + str(file_name)
        return None


              

# ..........***..........  Category Serializer ..........***..........


class CategorySerializer(serializers.ModelSerializer):
    # image = Base64ImageField()
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        exclude = ['slug']
        #fields = '__all__'

    def get_image_url(self, obj):
        if obj.image:
            file_name = obj.image
            return BASE_URL + str(file_name)
        else:
            return None


# ..........***..........  Category Serializer ..........***..........


class CategoryDetailsSerializer(serializers.ModelSerializer):
    food_list = serializers.SerializerMethodField(read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = Category
        fields = '__all__'

    def get_food_list(self, obj):
        if obj:
            serializer = FoodDetailSerializer(
                obj.foods, many=True)
            return serializer.data
        return None

    def get_image_url(self, obj):
        if obj.image:
            file_name = obj.image
            return BASE_URL + str(file_name)
        else:
            return None


# ..........***..........  Notification Serializer ..........***..........


class NotificationSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Notification
        fields = [
                  'id',
                  'title',
                  'description',
                  'image',
                  'image_url',
                  'created_at',
                  'updated_at',
                  ]   
        

    def get_image_url(self, obj):
        if obj.image:
            file_name =obj.image
            return BASE_URL + str(file_name)

                                           
# ..........***..........  Cafe Serializer ..........***..........


class CafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafe
        fields = '__all__'     
        
           
# ..........***..........  Cafe Serializer ..........***..........


class CafeCustomSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = Cafe
        fields = ['id','email','phone']
        
                
# ..........***.......... Cloud Cafe Information Start ..........***..........


class CloudCafeInformationSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField(read_only=True)
    cafe_details = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = CloudCafeInformation
        fields = '__all__'
        
    def get_logo_url(self,obj):
        if obj.logo:
            file_name = obj.logo 
            return BASE_URL + str(file_name)
        else:
            return None  
        
    def get_cafe_details(self,obj):
        qs = Cafe.objects.all()
        serializer = CafeSerializer(
            qs, many=True)
        return serializer.data

# ..........***.......... Food Extra..........***..........


class FoodExtraCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodExtra
        fields = [
            'title',
            'price'
        ]

# ..........***.......... Food Option..........***..........


class FoodOptionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodOption
        fields = [
            'title',
            'price'
        ]



# ..........***.......... Food Option..........***..........


class FoodOptionUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    title = serializers.CharField(required=True)
    price = serializers.FloatField(required=True)
        
# ..........***.......... Food Extra..........***..........


class FoodExtraUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    title = serializers.CharField(required=True)
    price = serializers.FloatField(required=True)


# ..........***.......... Food Option..........***..........


class FoodOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodOption
        fields = '__all__'

               

# ..........***.......... Food Extra..........***..........


class FoodExtraSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodExtra
        fields = '__all__'

# ..........***.......... Food ..........***..........


class FoodCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)
    food_option = serializers.ListSerializer(child=FoodOptionCreateSerializer())
    food_extra = serializers.ListSerializer(child=FoodExtraCreateSerializer(), required= False)

    class Meta:
        model = Food
        fields = [
            'title',
            'sub_title',
            'image',
            'category',
            'description',
            'is_active',
            'is_vat_applicable',
            'food_option',
            'food_extra',

        ]
        
    def create(self, validated_data):
        image = validated_data.pop('image', None)
        if image:
            return Food.objects.create(image=image, **validated_data)
        return Food.objects.create(**validated_data)
    

# ..........***.......... Food Details..........***..........


class FoodDetailSerializer(serializers.ModelSerializer):
    category_detail = serializers.SerializerMethodField(read_only=True)
    food_option = serializers.SerializerMethodField(read_only=True)
    food_extra = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    image_url = serializers.SerializerMethodField(read_only=True)

   
    class Meta:
        model = Food
        fields = [
            'id',
            'title',
            'sub_title',
            'price',
            'slug',
            'image',
            'image_url',
            'category',
            'category_detail',
            'description',
            'is_active',
            'is_vat_applicable',
            'food_option',
            'food_extra',
            'rating',
            'total_rating'
        ]


    def get_image_url(self, obj):
        if obj.image:
            file_name = obj.image
            return BASE_URL + str(file_name)
        else:
            return None

    def get_category_detail(self, obj):
        if obj.category:
            serializer = CategorySerializer(obj.category)
            return serializer.data
        return None

    def get_price(self, obj):
        option_qs = obj.food_options.order_by('price').first()
        if option_qs:
            return round(option_qs.price, 2)
        else:
            return None

    def get_food_option(self, obj):
        if obj.food_options:
            serializer = FoodOptionSerializer(obj.food_options,
                                              many=True)
            return serializer.data
        return None

    def get_food_extra(self, obj):
        if obj.food_extras:
            serializer = FoodExtraSerializer(obj.food_extras,
                                             many=True)
            return serializer.data
        return None
    
    
# ..........***.......... Food Update ..........***..........

class FoodUpdateSerializer(serializers.ModelSerializer):
    food_option = serializers.ListSerializer(child=FoodOptionUpdateSerializer())
    food_extra = serializers.ListSerializer(child=FoodExtraUpdateSerializer())
    
    class Meta:
        model = Food
        fields = [
            'title',
            'sub_title',
            'image',
            'category',
            'description',
            'is_active',
            'is_vat_applicable',
            'food_option',
            'food_extra'

        ]

    def get_food_option(self, obj):
        if obj.food_options:
            serializer = FoodOptionUpdateSerializer(obj.food_options,
                                              many=True)
            return serializer.data
        return None

    def get_food_extra(self, obj):
        if obj.food_extras:
            serializer = FoodExtraUpdateSerializer(obj.food_extras,
                                             many=True)
            return serializer.data
        return None
 

# ..........***..........  Review Serializer ..........***..........   


class ReviewSerializer(serializers.ModelSerializer):
    customer_info = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Review
        fields = '__all__' 
        
    def get_rating(self, obj):
        if obj:
            return obj.food_order.id
        else:
            return None  
        
    def get_customer_info(self, obj):
        if obj.customer:
            serializer = CustomerInfoSerializer(
                instance=obj.customer
            )
            return serializer.data
        return None              

# ..........***.......... Order Item..........***..........


class OrderedItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderedItem
        fields = [
            'quantity',
            'food_option',
            'food_extra'
        ]


class OrderedItemDetailSerializer(serializers.ModelSerializer):
    food_option_detail = serializers.SerializerMethodField(read_only=True)
    food_extra_detail = serializers.SerializerMethodField(read_only=True)
    food_image_url = serializers.SerializerMethodField(read_only=True)
    status_detail = serializers.CharField(source='get_status_display')
    food_name = serializers.CharField(
        source="food_option.food.title", read_only=True)

    class Meta:
        model = OrderedItem
        fields = [
            'id',
            'quantity',
            'food_name',
            'food_image_url',
            'food_option',
            'food_option_detail',
            'food_extra',
            'food_extra_detail',
            'status',
            'status_detail',
            'created_at',
            'updated_at'
        ]


    def get_food_image_url(self, obj):
        if obj.food_option.food.image:
            file_name = obj.food_option.food.image
            return BASE_URL + str(file_name)
        else:
            return None

    def get_food_option_detail(self,obj):
        if obj.food_option:
            serializer = FoodOptionSerializer(obj.food_option)
            return serializer.data
        return None

    def get_food_extra_detail(self,obj):
        if obj.food_extra:
            serializer = FoodExtraSerializer(obj.food_extra, many=True)
            return serializer.data
        return None

# ..........***.......... Food Order ..........***..........


class FoodOrderSerializer(serializers.ModelSerializer):
    review_details = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = FoodOrder
        fields = '__all__'

    def get_review_details(self,obj):
        serializer = ReviewSerializer(
            obj.reviews, many=True)
        return serializer.data        
        

class FoodOrderCreateSerializer(serializers.ModelSerializer):
    order_item = serializers.ListSerializer(child=OrderedItemCreateSerializer())

    class Meta:
        model = FoodOrder
        fields = [
            'remarks',
            'order_item'
        ]


class FoodOrderLogSerializer(serializers.ModelSerializer):
    staff_information = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FoodOrderLog
        fields = '__all__'

    def get_staff_information(self, obj):
        if obj:
            return {
                'id':obj.staff.id,
                'staff_id':obj.staff_id,
                'name':obj.staff.name,
                'phone':obj.staff.phone,
                'email':obj.staff.email,
                'cafe':obj.staff.cafe.name,
            }
        return None


class FoodOrderDetailSerializer(serializers.ModelSerializer):
    order_item_detail = serializers.SerializerMethodField(read_only=True)
    price_details = serializers.SerializerMethodField(read_only=True)
    status_detail = serializers.CharField(source='get_status_display')
    customer_detail = serializers.SerializerMethodField(read_only=True)
    cafe_detail = serializers.SerializerMethodField(read_only=True)
    food_order_log = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FoodOrder
        fields = [
            'id',
            'order_no',
            'remarks',
            'status',
            'status_detail',
            'order_item_detail',
            'grand_total',
            'vat_amount',
            'payable_amount',
            'price_details',
            'customer',
            'customer_detail',
            'cafe',
            'cafe_detail',
            'food_order_log',
            'created_at',
            'updated_at',
        ]

    def get_order_item_detail(self,obj):
        if obj.ordered_items:
            serializer = OrderedItemDetailSerializer(
                obj.ordered_items.exclude(status = 'CANCELLED'), many=True)
            return serializer.data
        return None

    def get_food_order_log(self,obj):
        if obj.food_order_logs:
            serializer = FoodOrderLogSerializer(obj.food_order_logs.last())
            return serializer.data
        return None

    def get_price_details(self, obj):
        calculate_price_with_initial_item = self.context.get(
            'calculate_price_with_initial_item', False)
        return calculate_price(product_order_obj=obj,
                               include_initial_order=calculate_price_with_initial_item)
        return None

    def get_customer_detail(self, obj):
        if obj.customer:
            serializer = CustomerInfoSerializer(obj.customer)
            return serializer.data
        return None

    def get_cafe_detail(self, obj):
        if obj.cafe:
            serializer = CafeSerializer(obj.cafe)
            return serializer.data
        return None


class FoodOrderPreparingSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()


class FoodOrderPickedSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    delivery_boy_id = serializers.IntegerField()


class OrderItemCancelSerializer(serializers.Serializer):
    order_item_id = serializers.IntegerField()


# ..........***..........  WishList Serializer ..........***..........


class WishListSerializer(serializers.ModelSerializer):
    customer_detail = serializers.SerializerMethodField(read_only=True)
    food_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WishList
        fields = '__all__'

    def get_customer_detail(self, obj):
        if obj.customer:
            serializer = CustomerInfoSerializer(obj.customer)
            return serializer.data
        return None

    def get_food_detail(self, obj):
        if obj.customer:
            serializer = FoodDetailSerializer(obj.food)
            return serializer.data
        return None
        
        
class WishListCreateSerializer(serializers.Serializer):
    food_id = serializers.IntegerField()
           
           