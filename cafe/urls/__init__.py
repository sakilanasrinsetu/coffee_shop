from .apps import apps_url
from .cafe import cafe_urls
from django.urls import include, path


urlpatterns = [
    path('dashboard/', include(cafe_urls)),
    path('apps/', include(apps_url)),


]