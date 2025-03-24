from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError

class Call(models.Model):
    origin = models.CharField(max_length=15)
    destination = models.CharField(max_length=15)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20)

    def clean(self):
        if self.start_time > self.end_time:
            raise ValidationError("O horário de início não pode ser maior que o horário de término.")
    
    @property
    def duration(self):
        return (self.end_time - self.start_time).total_seconds()

    def __str__(self):
        return f"{self.origin} -> {self.destination} ({self.status})"

class CallMetric(models.Model):
    total_calls = models.IntegerField()
    total_duration = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)