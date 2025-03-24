from django.contrib import admin
from .models import Call, CallMetric


class MailingAdmin(admin.ModelAdmin):
    list_display = ("origin", "destination", "start_time", "end_time", "status")
    search_fields = ("status", "origin", "destination")

admin.site.register(Call, MailingAdmin)
admin.site.register(CallMetric)
