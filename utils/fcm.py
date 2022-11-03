
from accounts.models import *
import datetime
import json

import requests
from django.conf import settings

# from fcm_django.models import FCMDevice


# FCM_DJANGO_SETTINGS = {
#     "FCM_SERVER_KEY": "AAAA0HAEqOY:APA91bH5tJDGmxbdt7cZgVyImj-QU1tvIFpq3EfkiQZgmj-ktSRMNJkonGnZiVoKAVH9bT80Y-TFs22u4F5O46d97xQn90CE0FEnItifG6cofZt0_IorqX2N7sZwaUgUBvzGwE5aZ9Kt",
#     "ONE_DEVICE_PER_USER": True,
#     "DELETE_INACTIVE_DEVICES": False,
# }


FCM_SERVER_KEY = settings.FCM_DJANGO_SETTINGS.get('FCM_SERVER_KEY')


def send_fcm_push_notification_appointment(tokens_list: list, status="CallStaff",
                                           table_no=0, msg='', staff_id_list: list = list(),
                                           qs=None, **kwargs):

    order_no = kwargs.get('order_no')
    food_name = kwargs.get(('food_name'))
    food_name_list = kwargs.get('food_names', [])
    food_name_str = ' ,'.join(map(str, food_name_list))
    tokens_list = list(set(tokens_list))
    message_title = kwargs.get(('message_title'))
    message_body = kwargs.get(('message_body'))

    status_value = {
        "Received": {
            'notification': {'title': 'Received',
                             'body': f'An order has been placed for table {str(table_no)}'},
            'data': {'title': '1', 'body': str(datetime.datetime.now())}
        },
        'Cooking': {
            'notification': {'title': 'Order Verified',
                             'body': f'Your food is preparing'},
            'data': {'title': 'Order Verified',
                             'body': f'Your food is preparing'}
        },
        'WaiterHand': {
            'notification': {'title': 'WaiterHand',
                             'body': f'Your food is ready for serving {str(datetime.datetime.now())}'},
            'data': {'title': '3', 'body': str(datetime.datetime.now())}
        },
        'Delivered': {
            'notification': {'title': 'Delivered',
                             'body': f'Food has been delivered {str(datetime.datetime.now())}'},
            'data': {'title': '5', 'body': str(datetime.datetime.now())}
        },
        'Rejected': {
            'notification': {'title': 'Rejected',
                             'body': f'Your food is rejected by kitchen {str(datetime.datetime.now())}'},
            'data': {'title': '6', 'body': str(datetime.datetime.now())}
        },
        'CallStaff': {
            'notification': {'title': 'Calling Waiter',
                             #  'image': "http://manager.i-host.com.bd/logo.png",
                             'body': f'Customer from table no {str(table_no)} is looking for you'},
            'data': {'title': 'Calling Waiter',
                     #  'image': "http://manager.i-host.com.bd/logo.png",
                     'body': f'Customer from table no {str(table_no)} is looking for you'},

        },
        'CallStaffForPayment': {
            'notification': {'title': 'Calling Waiter for payment',
                             'body': f'Customer from table no {str(table_no)} is looking for you for {str(msg)} payment'},
            'data': {'title': '8', 'body': str(datetime.datetime.now())}
        },
        'OrderCancel': {
            'notification': {'title': 'Order Cancel',
                             'body': f'Your order has been cancelled'},
            'data': {'title': '9', 'body': str(datetime.datetime.now())}
        },
        'OrderItemsCancel': {
            'notification': {'title': 'Item cancel',
                             'body': f'{food_name_str} has been cancelled from your cart'},
            'data': {'title': '9', 'body': str(datetime.datetime.now())}
        },
        'OrderItemCancel': {
            'notification': {'title': 'Item cancel',
                             'body': f'{food_name} has been cancelled from your cart'},
            'data': {'title': '9', 'body': str(datetime.datetime.now())}
        },
        'Message': {
            'notification': {'title': f'{message_title}',
                             'body': f'{message_body}'},
            'data': {'title': '9',
                     'body': str(datetime.datetime.now())}
        },

        'OrderComplete': {
            'notification': {'title': 'Order Complete',
                             'body': f'Your order has been completed'},
            'data': {'title': '9', 'body': str(datetime.datetime.now())}
        },


    }
    success = False
    if status == "SendCustomerAdvertisement":
        status_value["SendCustomerAdvertisement"] = {
            'notification': {'title': qs.title if qs else None,
                             'body': qs.body if qs else None,
                             'image': qs.image if qs else None,
                             },
            'data': qs.data if qs else None,
        }

    try:

        data = {
            "notification": status_value[status]['notification'],
            "data": status_value[status]['data'],
            "apns": {
                "headers": {
                    'apns-priority': '10',
                },
                "payload": {
                    "aps": {
                        "sound": 'default',
                    },
                },
            },
            "registration_ids": tokens_list
        }
        headers = {
            'Content-type': 'application/json',
            'Authorization': 'key=' + str(FCM_SERVER_KEY)
        }
        response = requests.post(
            'https://fcm.googleapis.com/fcm/send', data=json.dumps(data), headers=headers)
        # print("Fcm Response ", response)
        if 300 > response.status_code >= 200:
            if response.json().get('success') >= 1:
                success = True
        if success:
            fcm_notification_staff_obj_list = list()
            for staff_id in staff_id_list:
                fcm_notification_staff_obj_list.append(
                    FcmNotificationStaff(staff_device_id=staff_id, data=status_value.get(status)))
            if fcm_notification_staff_obj_list:
                FcmNotificationStaff.objects.bulk_create(
                    fcm_notification_staff_obj_list, ignore_conflicts=True)

    except Exception as e:
        # print("FCm Exception ", e)
        # done
        pass

    return success
