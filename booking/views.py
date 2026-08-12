import logging

from django.db import transaction
from django.db.models import Exists, OuterRef

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BookingRequest, LSAProfile, Payment
from .serializers import BookingSerializer


class BookingCreateView(APIView):

    @transaction.atomic
    def post(self, request):

        serializer = BookingSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        data = serializer.validated_data

        overlapping_booking = BookingRequest.objects.filter(
            lsa=data["lsa"],
            status__in=[
                "PENDING",
                "CONFIRMED",
            ],
            start_time__lt=data["end_time"],
            end_time__gt=data["start_time"],
        ).exists()

        if overlapping_booking:

            return Response(
                {
                    "error": (
                        "LSA is already booked "
                        "during this time."
                    )
                },
                status=status.HTTP_409_CONFLICT,
            )

        booking = serializer.save()

        return Response(
            BookingSerializer(booking).data,
            status=status.HTTP_201_CREATED,
        )

class LSASearchView(APIView):

     def get(self, request):

        skill = request.GET.get("skill")
        start_time = request.GET.get("start_time")
        end_time = request.GET.get("end_time")

        queryset = LSAProfile.objects.filter(
            is_active=True
        )

        if skill:
            queryset = queryset.filter(
                skills__icontains=skill
            )

        if start_time and end_time:

            conflicting_bookings = BookingRequest.objects.filter(
                lsa=OuterRef("pk"),
                status__in=[
                    "PENDING",
                    "CONFIRMED",
                ],
                start_time__lt=end_time,
                end_time__gt=start_time,
            )

            queryset = queryset.annotate(
                has_conflict=Exists(
                    conflicting_bookings
                )
            ).filter(
                has_conflict=False
            )

        return Response(
            list(
                queryset.values(
                    "id",
                    "name",
                    "email",
                    "skills",
                    "hourly_rate",
                )
            )
        )

logger = logging.getLogger(__name__)


class PaymentWebhookView(APIView):

    @transaction.atomic
    def post(self, request):

        booking_id = request.data.get("booking_id")
        transaction_id = request.data.get("transaction_id")
        payment_status = request.data.get("status")
        amount = request.data.get("amount")

        if not booking_id:
            return Response(
                {"error": "booking_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not transaction_id:
            return Response(
                {"error": "transaction_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if payment_status not in ["SUCCESS", "FAILED"]:
            return Response(
                {
                    "error": (
                        "status must be SUCCESS or FAILED."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            booking = BookingRequest.objects.get(
                id=booking_id
            )
        except BookingRequest.DoesNotExist:
            return Response(
                {"error": "Booking not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        payment, created = Payment.objects.update_or_create(
            booking=booking,
            defaults={
                "transaction_id": transaction_id,
                "amount": amount,
                "status": payment_status,
            },
        )

        if payment_status == "SUCCESS":
            booking.status = "CONFIRMED"
        else:
            booking.status = "FAILED"

        booking.save(
            update_fields=["status"]
        )

        logger.info(
            "Payment webhook processed: booking=%s status=%s",
            booking.id,
            payment_status,
        )

        return Response(
            {
                "message": "Payment webhook processed.",
                "booking_id": booking.id,
                "payment_id": payment.id,
                "payment_status": payment.status,
                "booking_status": booking.status,
            },
            status=status.HTTP_200_OK,
        )