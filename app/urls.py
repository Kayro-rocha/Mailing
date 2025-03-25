from django.contrib import admin
from django.urls import path
from mailing.views import call_list, call_list_api, call_metrics, get_alerts

urlpatterns = [
    path('admin/', admin.site.urls),
    path('call/', call_list, name='call_list'),
    path('api/calls/', call_list_api, name='call_list_api'),
    path('api/metrics/', call_metrics, name='call_metrics'),
    path('api/alerts/', get_alerts, name='get_alerts'),
]
