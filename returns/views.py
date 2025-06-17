from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .models import ReturnRequest, RefundRequest, Dispute
from .serializers import ReturnRequestSerializer, RefundRequestSerializer, DisputeSerializer

from django.shortcuts import render, redirect
from .forms import ReturnRequestForm, RefundRequestForm, DisputeForm


class ReturnRequestViewSet(viewsets.ModelViewSet):
    queryset = ReturnRequest.objects.all().order_by('-submitted_at')
    serializer_class = ReturnRequestSerializer

    @action(detail=True, methods=["patch"], permission_classes=[IsAdminUser])
    def update_status(self, request, pk=None):
        return_request = self.get_object()
        data = request.data

        status_choice = data.get("return_status")
        refund_choice = data.get("refund_type")

        valid_statuses = dict(ReturnRequest.RETURN_STATUS_CHOICES).keys()
        valid_refunds = dict(ReturnRequest._meta.get_field("refund_type").choices).keys()

        errors = {}

        if status_choice not in valid_statuses:
            errors["return_status"] = f"'{status_choice}' is not a valid status."

        if refund_choice not in valid_refunds:
            errors["refund_type"] = f"'{refund_choice}' is not a valid refund type."

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        return_request.return_status = status_choice
        return_request.refund_type = refund_choice
        return_request.save()

        return Response(
            {
                "message": "Return request updated successfully.",
                "return_status": status_choice,
                "refund_type": refund_choice,
            },
            status=status.HTTP_200_OK
        )

def submit_return(request):
    if request.method == "POST":
        form = ReturnRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("success-page")
    else:
        form = ReturnRequestForm()

    return render(request, "return_form.html", {"form": form})

def return_success(request):
    return render(request, "success.html")

def submit_refund(request):
    if request.method == "POST":
        form = RefundRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("success")
    else:
        form = RefundRequestForm()
    return render(request, "refund_form.html", {"form": form})

def submit_dispute(request):
    if request.method == "POST":
        form = DisputeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("success")
    else:
        form = DisputeForm()
    return render(request, "dispute_form.html", {"form": form})

class RefundRequestViewSet(viewsets.ModelViewSet):
    queryset = RefundRequest.objects.all().order_by('-processed_at')
    serializer_class = RefundRequestSerializer

class DisputeViewSet(viewsets.ModelViewSet):
    queryset = Dispute.objects.all().order_by('-submitted_at')
    serializer_class = DisputeSerializer