from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from .models import (
    Parent,
    LSAProfile,
    BookingRequest,
    Payment,
)


class BookingAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Create test parent
        self.parent = Parent.objects.create(
            name="Test Parent",
            email="parent@test.com",
            phone="9876543210",
        )

        # Create test LSA
        self.lsa = LSAProfile.objects.create(
            name="Test LSA",
            email="lsa@test.com",
            skills=["autism", "reading", "dyslexia"],
            hourly_rate=500,
            is_active=True,
        )

        # Future booking time
        self.start_time = (
            timezone.now()
            + timedelta(days=1)
        ).replace(
            minute=0,
            second=0,
            microsecond=0,
        )

        self.end_time = (
            self.start_time
            + timedelta(hours=1)
        )

    # Test 1
    def test_booking_creation_success(self):

        response = self.client.post(
            "/api/v1/bookings/",
            {
                "parent": self.parent.id,
                "lsa": self.lsa.id,
                "start_time": self.start_time.isoformat(),
                "end_time": self.end_time.isoformat(),
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        self.assertEqual(
            response.data["parent"],
            self.parent.id,
        )

        self.assertEqual(
            response.data["lsa"],
            self.lsa.id,
        )

    # Test 2
    def test_invalid_booking_data(self):

        response = self.client.post(
            "/api/v1/bookings/",
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    # Test 3
    def test_double_booking(self):

        # Existing booking
        BookingRequest.objects.create(
            parent=self.parent,
            lsa=self.lsa,
            start_time=self.start_time,
            end_time=self.end_time,
            status="PENDING",
        )

        # Overlapping booking request
        response = self.client.post(
            "/api/v1/bookings/",
            {
                "parent": self.parent.id,
                "lsa": self.lsa.id,
                "start_time": (
                    self.start_time
                    + timedelta(minutes=30)
                ).isoformat(),
                "end_time": (
                    self.end_time
                    + timedelta(minutes=30)
                ).isoformat(),
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            409,
        )

    # Test 4
    def test_lsa_search(self):

        response = self.client.get(
            "/api/v1/lsas/search/",
            {
                "skill": "autism",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["name"],
            "Test LSA",
        )

    # Test 5
    def test_payment_webhook_success(self):

        booking = BookingRequest.objects.create(
            parent=self.parent,
            lsa=self.lsa,
            start_time=self.start_time,
            end_time=self.end_time,
            status="PENDING",
        )

        response = self.client.post(
            "/api/v1/payments/webhook/",
            {
                "booking_id": booking.id,
                "transaction_id": "TEST_TXN_001",
                "status": "SUCCESS",
                "amount": "500.00",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        booking.refresh_from_db()

        self.assertEqual(
            booking.status,
            "CONFIRMED",
        )

        payment = Payment.objects.get(
            booking=booking
        )

        self.assertEqual(
            payment.status,
            "SUCCESS",
        )