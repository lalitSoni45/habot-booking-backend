from django.db import models


class Parent(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class LSAProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    skills = models.JSONField(default=list)
    hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class BookingRequest(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
        ("FAILED", "Failed"),
    ]

    parent = models.ForeignKey(
        Parent,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    lsa = models.ForeignKey(
        LSAProfile,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(
                fields=["lsa", "start_time", "end_time"]
            ),
            models.Index(
                fields=["status"]
            ),
        ]

    def __str__(self):
        return f"{self.parent} - {self.lsa}"


class Payment(models.Model):

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
    ]

    booking = models.OneToOneField(
        BookingRequest,
        on_delete=models.CASCADE,
        related_name="payment"
    )

    transaction_id = models.CharField(
        max_length=100,
        unique=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id