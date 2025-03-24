from django.core.management.base import BaseCommand
from mailing.models import Call
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Popula o banco de dados com chamadas falsas'

    def handle(self, *args, **kwargs):
        self.generate_fake_calls()

    def generate_fake_calls(self, num_calls=10):
        """ Gera chamadas falsas para popular o banco de dados """
        calls = []
        for _ in range(num_calls):
            start_time = datetime.now() - timedelta(minutes=random.randint(1, 120))
            duration = random.randint(30, 600)  # Entre 30 segundos e 10 minutos
            end_time = start_time + timedelta(seconds=duration)

            call = Call(
                origin=f"+55{random.randint(1000000000, 9999999999)}",
                destination=f"+55{random.randint(1000000000, 9999999999)}",
                start_time=start_time,
                end_time=end_time,
                status=random.choice(["Atendida", "Perdida", "Encerrada"])
            )
            calls.append(call)

        # Cria as chamadas no banco de dados
        Call.objects.bulk_create(calls)
        self.stdout.write(self.style.SUCCESS(f'{num_calls} chamadas criadas com sucesso!'))
