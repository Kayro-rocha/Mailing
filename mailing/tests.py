from django.test import TestCase
from .models import Call
from django.utils.timezone import now, timedelta
from django.core.exceptions import ValidationError

class CallTestCase(TestCase):
    def setUp(self):
        Call.objects.create(
            origin="111111111",
            destination="222222222",
            start_time=now(),
            end_time=now() + timedelta(minutes=5),
            status="completed"
        )

    def test_normal_case(self):
        call = Call.objects.get(origin="111111111")
        self.assertEqual(call.status, "completed")
        self.assertEqual(call.duration, 300)
    
    def test_border_case(self):
        call = Call.objects.create(
            origin="333333333",
            destination="444444444",
            start_time=now(),
            end_time=now(),
            status="completed"
        )
        self.assertEqual(call.duration, 0)

    def test_exceptional_case(self):
        call = Call(
            origin="555555555",
            destination="666666666",
            start_time=now() + timedelta(minutes=5),
            end_time=now(),
            status="completed"
        )
        with self.assertRaises(ValidationError):
            call.full_clean()