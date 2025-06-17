from django.contrib import admin
from .models import ReturnRequest, RefundRequest, Dispute

admin.site.register(ReturnRequest)
admin.site.register(RefundRequest)
admin.site.register(Dispute)
