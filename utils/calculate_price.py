import decimal
from dashboard.models import *
from cafe.models import *
import dashboard
from django.utils import timezone
from datetime import date, datetime, timedelta
import datetime
from django.utils import timezone
from datetime import datetime


def calculate_price(product_order_obj, include_initial_order=False, **kwargs):
    cafe_qs = Cafe.objects.filter(id = product_order_obj.cafe.id).last()
    cloud_cafe_information_qs = CloudCafeInformation.objects.all().last()
    total_price = 0.0
    grand_total_price = 0.0
    hundred = 100.00
    vat_charge = 0.0
    vat_amount = 0.0
    delivery_charge = 0.0

    today = timezone.now()
    current_time = datetime.now().time()

    ordered_items_qs = product_order_obj.ordered_items.exclude(
            status__in=["CANCELLED"]
        )

    for ordered_item in ordered_items_qs:
        item_price = ordered_item.quantity * ordered_item.food_option.price
        extra_price = ordered_item.quantity * sum(
            list(
                ordered_item.food_extra.values_list('price', flat=True)
            )
        )
        total_price += item_price + extra_price

    # total price save in database

    vat_charge += cloud_cafe_information_qs.vat_amount
    delivery_charge += cloud_cafe_information_qs.delivery_amount
    vat_amount = vat_charge * total_price/hundred

    grand_total_price = total_price
    payable_amount = grand_total_price + vat_amount + delivery_charge

    product_order_obj.grand_total = grand_total_price
    product_order_obj.payable_amount = payable_amount
    product_order_obj.save()

    vat_charge = str(vat_charge)+'%'

    response_dict = {
        "product_total_price": round(total_price, 2),
        'vat_charge': vat_charge,
        'vat_amount': round(vat_amount, 2),
        'delivery_charge': round(delivery_charge, 2),
        'payable_amount': round(payable_amount, 2)
    }

    return response_dict


