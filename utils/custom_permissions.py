from django.db.models import Q
from cafe.models import Cafe
from accounts.models import CafeStaffInformation, UserAccount
from rest_framework import permissions

"""
[summary]
        # self.check_object_permissions(request, obj=1) #its cafe_id
Returns
-------
[type]
    [description]
"""


class IsCafeManager(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    message = 'Not a Cafe Manager.'

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if not bool(request.user and request.user.is_authenticated):
            return False

        cafe_staff_qs = CafeStaffInformation.objects.filter(
            user=request.user, is_manager=True)
        if cafe_staff_qs:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if not bool(request.user and request.user.is_authenticated):
            return False

        cafe_staff_qs = CafeStaffInformation.objects.filter(
            cafe=obj, user=request.user, is_manager =True)
        if cafe_staff_qs:
            return True
        else:
            return False


class IsCafeBarista(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    message = 'Not a Cafe Barista.'

    # def has_permission(self, request, view):
    #     """
    #     Return `True` if permission is granted, `False` otherwise.
    #     """

    #     return False
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """

        if not bool(request.user and request.user.is_authenticated):
            return False
        cafe_staff_qs = CafeStaffInformation.objects.filter(
            user=request.user, is_barista=True)
        if cafe_staff_qs:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if not bool(request.user and request.user.is_authenticated):
            return False

        cafe_staff_qs = CafeStaffInformation.objects.filter(
            cafe=obj, user_id=request.user.pk, is_barista=True)
        if cafe_staff_qs:
            return True
        else:
            return False


class IsCafeDeliveryBoy(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    message = 'Not a Cafe Delivery Boy.'

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if not bool(request.user and request.user.is_authenticated):
            return False

        cafe_staff_qs = CafeStaffInformation.objects.filter(
            user=request.user, is_delivery_boy=True)
        if cafe_staff_qs:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if not bool(request.user and request.user.is_authenticated):
            return False

        cafe_staff_qs = CafeStaffInformation.objects.filter(
            Cafe=obj, user=request.user, is_delivery_boy=True)
        if cafe_staff_qs:
            return True
        else:
            return False


class IsCafeStaff(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    message = 'Not a Cafe staff.'

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if not bool(request.user and request.user.is_authenticated):
            return False

        cafe_staff_qs = CafeStaffInformation.objects.filter(
            Q(user=request.user), Q(is_waiter=True) | Q(is_owner=True) | Q(is_manager=True))
        if cafe_staff_qs:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # cafe_staff_qs = HotelStaffInformation.objects.filter(
        #     Cafe=obj, user=request.user, is_waiter=True)
        if not bool(request.user and request.user.is_authenticated):
            return False

        cafe_staff_qs = CafeStaffInformation.objects.filter(
            Q(user=request.user, Cafe=obj), Q(is_waiter=True) | Q(is_owner=True) | Q(is_manager=True))

        if cafe_staff_qs:
            return True
        else:
            return False


class IsCafeManagerOrAdmin(permissions.IsAuthenticated):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    message = 'Not a Cafe staff.'

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if not bool(request.user and request.user.is_authenticated):
            return False

        if request.user.is_staff or request.user.is_superuser:
            return True
        cafe_staff_qs = CafeStaffInformation.objects.filter(
            Q(user=request.user), Q(is_manager=True) | Q(user__is_staff=True) | Q(user__is_superuser=True))
        if cafe_staff_qs:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # cafe_staff_qs = CafeStaffInformation.objects.filter(
        #     Cafe=obj, user=request.user, is_waiter=True)

        if not bool(request.user and request.user.is_authenticated):
            return False

        if UserAccount.objects.filter(Q(is_staff=True) | Q(is_superuser=True), pk=request.user.pk):
            return True

        cafe_staff_qs = CafeStaffInformation.objects.filter(
            Q(user=request.user, Cafe=obj),   Q(is_owner=True) | Q(is_manager=True))

        if cafe_staff_qs:
            return True
        else:
            return False


class IsSuperAdminOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    message = 'Not a Cafe Admin or Super Admin'

    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False

        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.user.is_staff or request.user.is_superuser:
            return True
        cafe_staff_qs = CafeStaffInformation.objects.filter(
            Q(is_staff=True) | Q(user__is_superuser=True))
        if cafe_staff_qs:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # cafe_staff_qs = CafeStaffInformation.objects.filter(
        #     Cafe=obj, user=request.user, is_waiter=True)
        if not bool(request.user and request.user.is_authenticated):
            return False

        if UserAccount.objects.filter(Q(is_staff=True) | Q(is_superuser=True), pk=request.user.pk):
            return True

        cafe_staff_qs = CafeStaffInformation.objects.filter(
            Q(user=request.user, Cafe=obj),   Q(is_staff=True))

        if cafe_staff_qs:
            return True
        else:
            return False