from rest_framework import serializers
from .models import ReturnRequest, RefundRequest, Dispute

class ReturnRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnRequest
        fields = '__all__'
        read_only_fields = ['return_status', 'refund_type', 'submitted_at']

    def create(self, validated_data):
        # Extract important fields
        condition = validated_data.get('product_condition')
        within_period = validated_data.get('within_return_period')

        # Default decision logic
        if condition == 'damaged':
            validated_data['return_status'] = 'rejected'
            validated_data['refund_type'] = 'none'
        elif not within_period:
            validated_data['return_status'] = 'rejected'
            validated_data['refund_type'] = 'none'
        elif condition == 'good' and within_period:
            validated_data['return_status'] = 'approved'
            validated_data['refund_type'] = 'full'
        else:
            validated_data['return_status'] = 'pending'
            validated_data['refund_type'] = 'partial'

        return super().create(validated_data)

class RefundRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefundRequest
        fields = '__all__'

class DisputeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispute
        fields = '__all__'
