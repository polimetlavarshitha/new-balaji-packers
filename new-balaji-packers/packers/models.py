from django.db import models


class Branch(models.Model):
    """
    Branch locations for New Balaji Packers and Movers.
    Head office is Vuyyuru. Other branches are Vijayawada and Machilipatnam.
    """
    city = models.CharField(max_length=100)
    is_head_office = models.BooleanField(default=False, verbose_name="Head Office / Main Branch")
    badge = models.CharField(max_length=100, default="Branch Office")
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, default='')
    order = models.PositiveIntegerField(default=0, help_text="Display order on website")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"
        ordering = ['order', '-is_head_office', 'city']

    def __str__(self):
        head_tag = " (Head Office)" if self.is_head_office else ""
        return f"{self.city}{head_tag} - {self.phone}"


class BookingOrder(models.Model):
    """
    Booking quote and shifting orders placed by customers.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending Request'),
        ('CONFIRMED', 'Booking Confirmed'),
        ('IN_TRANSIT', 'In Transit / Shifting'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    name = models.CharField(max_length=150, verbose_name="Full Name")
    phone = models.CharField(max_length=20, verbose_name="Phone Number")
    email = models.EmailField(blank=True, null=True, verbose_name="Email Address")
    pickup_city = models.CharField(max_length=100, verbose_name="Pickup Location (From)")
    drop_city = models.CharField(max_length=100, verbose_name="Drop Location (To)")
    move_date = models.DateField(null=True, blank=True, verbose_name="Moving Date")
    selected_items = models.TextField(blank=True, verbose_name="Selected Items", help_text="Comma-separated selected items")
    custom_items = models.TextField(blank=True, verbose_name="Custom / Extra Items", help_text="Custom items typed manually by customer")
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Estimated Price (INR)")
    notes = models.TextField(blank=True, null=True, verbose_name="Additional Notes / Instructions")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Order Status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Booking Order"
        verbose_name_plural = "Booking Orders"
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.name} ({self.pickup_city} -> {self.drop_city})"


class CustomerReview(models.Model):
    """
    Verified customer reviews and ratings.
    """
    RATING_CHOICES = [
        (5, '5 Stars - Excellent'),
        (4, '4 Stars - Very Good'),
        (3, '3 Stars - Good'),
        (2, '2 Stars - Fair'),
        (1, '1 Star - Poor'),
    ]

    reviewer_name = models.CharField(max_length=120, verbose_name="Reviewer Name")
    city = models.CharField(max_length=100, blank=True, default="", verbose_name="City / Route")
    rating = models.IntegerField(choices=RATING_CHOICES, default=5, verbose_name="Rating")
    review_text = models.TextField(verbose_name="Review Message")
    is_approved = models.BooleanField(default=True, verbose_name="Approved for Display")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Customer Review"
        verbose_name_plural = "Customer Reviews"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reviewer_name} ({self.rating}★) - {self.city or 'General'}"
