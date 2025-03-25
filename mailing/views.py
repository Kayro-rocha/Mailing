from django.shortcuts import render
from django.http import JsonResponse
from .models import Call, CallMetric
from django.db.models import Sum
from django.utils.timezone import now
from django.db.models import F, ExpressionWrapper, fields
from django.db.models.functions import ExtractSecond
from datetime import timedelta


def call_list(request):
    calls = Call.objects.all()
    return render(request, 'dados.html', {'calls': calls})

def get_alerts(request):
    # Calcula a duração da chamada em segundos
    long_calls = Call.objects.annotate(
    duration_seconds=ExtractSecond(F('end_time') - F('start_time'))
    ).filter(duration_seconds__gt=300).count()
    active_calls = Call.objects.filter(start_time__lte=now(), end_time__isnull=True).count()

    alerts = []
    if long_calls > 0:
        alerts.append(f"{long_calls} chamadas com duração acima de 5 minutos.")
    if active_calls > 10:
        alerts.append(f"{active_calls} chamadas ativas simultaneamente!")

    return JsonResponse({"alerts": alerts})

def call_list_api(request):
    calls = list(Call.objects.values())
    return JsonResponse(calls, safe=False)

def format_duration(duration):
    """Formata um objeto timedelta em HH:MM:SS."""
    if isinstance(duration, timedelta):
        total_seconds = int(duration.total_seconds())
    else:
        total_seconds = int(duration)

    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def call_metrics(request):
    # Anotar a duração das chamadas
    calls_with_duration = Call.objects.annotate(
        duration=ExpressionWrapper(F('end_time') - F('start_time'), output_field=fields.DurationField())
    )

    # Filtrar chamadas curtas (< 5 min) e longas (>= 5 min)
    short_calls = calls_with_duration.filter(duration__lt="00:05:00").count()
    long_calls = calls_with_duration.filter(duration__gte="00:05:00").count()

    # Estatísticas gerais
    total_calls = Call.objects.count()
    total_duration = calls_with_duration.aggregate(total_duration=Sum('duration'))['total_duration'] or timedelta(0)

    # Converter total_duration para segundos (para o gráfico)
    total_duration_seconds = int(total_duration.total_seconds()) if total_duration else 0


    return JsonResponse({
        'short_calls': short_calls,
        'long_calls': long_calls,
        'total_calls': total_calls,
        'total_duration': format_duration(total_duration),  # HH:MM:SS
    })


