from django import forms
from .models import ReturnRequest, RefundRequest, Dispute

class ReturnRequestForm(forms.ModelForm):
    class Meta:
        model = ReturnRequest
        fields = [
            "customer_name",
            "order_id",
            "reason_for_return",
            "product_condition",
            "within_return_period",
            "image_url",
        ]

        widgets = {
            "reason_for_return": forms.Textarea(attrs={"rows": 4}),
            "product_condition": forms.Select(attrs={"class": "form-select"}),
        }

class RefundRequestForm(forms.ModelForm):
    class Meta:
        model = RefundRequest
        fields = [
            "return_request",
            "refund_amount",
            "processed_by",
            "notes",
        ]

class DisputeForm(forms.ModelForm):
    class Meta:
        model = Dispute
        fields = [
            "refund_request",
            "customer_name",
            "reason",
            "resolution_notes",
        ]
