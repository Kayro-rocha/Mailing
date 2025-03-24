from django.shortcuts import render
from django.http import JsonResponse
from .models import Call, CallMetric
from django.db.models import Sum

def call_list(request):
    calls = Call.objects.all()
    return render(request, 'dados.html', {'calls': calls})

def call_list_api(request):
    calls = list(Call.objects.values())
    return JsonResponse(calls, safe=False)

def format_duration(seconds):
    if seconds < 60:
        return f"{seconds} segundos"
    elif seconds < 3600:
        return f"{seconds // 60} minutos {seconds % 60} segundos"
    else:
        return f"{seconds // 3600} horas {(seconds % 3600) // 60} minutos"

def call_metrics(request):
    calls = Call.objects.all()
    total_calls = calls.count()
    total_duration = sum(call.duration for call in calls)
    total_duration_formatted = format_duration(int(total_duration))
    CallMetric.objects.create(total_calls=total_calls, total_duration=total_duration)
    return JsonResponse({'total_calls': total_calls, 'total_duration': total_duration_formatted})


