from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReturnRequestViewSet, RefundRequestViewSet, DisputeViewSet, submit_return, submit_refund, submit_dispute, return_success
from django.shortcuts import render  # ✅ Add this import


router = DefaultRouter()
router.register(r"returns", ReturnRequestViewSet)
router.register(r"refunds", RefundRequestViewSet)
router.register(r"disputes", DisputeViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("submit/", submit_return, name="submit-return"),  
    path("refund/submit/", submit_refund, name="submit-refund"),
    path("dispute/submit/", submit_dispute, name="submit-dispute"),
    # path("success/", lambda request: render(request, "success.html"), name="success-page"),
    path("success/", return_success, name="success"),
]
