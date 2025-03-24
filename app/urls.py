from django.contrib import admin
from django.urls import path
from mailing.views import call_list, call_list_api, call_metrics

urlpatterns = [
    path('admin/', admin.site.urls),
    path('call/', call_list, name='call_list'),
    path('api/calls/', call_list_api, name='call_list_api'),
    path('api/metrics/', call_metrics, name='call_metrics'),
]
