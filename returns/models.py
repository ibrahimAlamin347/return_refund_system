from django.db import models

class ReturnRequest(models.Model):
    RETURN_STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('partial_refund', 'Partial Refund'),
        ('full_refund', 'Full Refund'),
        ('no_refund', 'No Refund'),
    ]

    REFUND_TYPE_CHOICES = [
        ('full', 'Full Refund'),
        ('partial', 'Partial Refund'),
        ('none', 'No Refund'),
    ]

    PRODUCT_CONDITION_CHOICES = [
        ('good', 'Good'),
        ('damaged', 'Damaged'),
    ]

    customer_name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    order_id = models.CharField(max_length=50, unique=True)
    reason_for_return = models.TextField()

    product_condition = models.CharField(
        max_length=50,
        choices=PRODUCT_CONDITION_CHOICES,
        default='good'
    )
    within_return_period = models.BooleanField(default=True)

    image_url = models.URLField(blank=True, null=True, help_text="Optional image of the product")
    submitted_at = models.DateTimeField(auto_now_add=True)

    return_status = models.CharField(
        max_length=20,
        choices=RETURN_STATUS_CHOICES,
        default='pending'
    )
    refund_type = models.CharField(
        max_length=50,
        choices=REFUND_TYPE_CHOICES,
        default='none'
    )

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Return Request"
        verbose_name_plural = "Return Requests"

    def __str__(self):
        return f"{self.product_name} return by {self.customer_name} — Status: {self.return_status}"

    def save(self, *args, **kwargs):
        # Decision logic for refund type
        if self.within_return_period:
            if self.product_condition == 'good':
                self.refund_type = 'full'
                self.return_status = 'approved'
            elif self.product_condition == 'damaged':
                self.refund_type = 'partial'
                self.return_status = 'partial_refund'
        else:
            self.refund_type = 'none'
            self.return_status = 'rejected'
        super().save(*args, **kwargs)

class RefundRequest(models.Model):
    return_request = models.OneToOneField(ReturnRequest, on_delete=models.CASCADE, related_name='refund_request')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    processed_at = models.DateTimeField(auto_now_add=True)
    processed_by = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-processed_at']
        verbose_name = "Refund Request"
        verbose_name_plural = "Refund Requests"

    def __str__(self):
        return f"Refund for {self.return_request.order_id} - Amount: {self.refund_amount}"

class Dispute(models.Model):
    refund_request = models.ForeignKey(RefundRequest, on_delete=models.CASCADE, related_name='disputes')
    customer_name = models.CharField(max_length=100)
    reason = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Dispute"
        verbose_name_plural = "Disputes"

    def __str__(self):
        return f"Dispute by {self.customer_name} for Refund {self.refund_request.id}"
