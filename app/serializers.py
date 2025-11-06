from rest_framework import serializers
from .models import Client, Installment, BurialRecord, Payment

# Installment Serializer
class InstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installment
        fields = ['id', 'installment_number', 'amount', 'due_date', 'paid']

# Payment Serializer
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'date', 'installment']

class ClientSerializer(serializers.ModelSerializer):
    installments = InstallmentSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    amount_paid = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    remaining_balance = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Client
        fields = [
            'id',
            'name',
            'lot_number',
            'payment_scheme',
            'total_price',
            'contact_number',    
            'address',           
            'installments',
            'payments',
            'amount_paid',
            'remaining_balance'
        ]




class BurialRecordSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)  # Nested client details
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(), source='client', write_only=True
    )

    class Meta:
        model = BurialRecord
        fields = [
            'id',
            'deceased_name',
            'date_of_death',
            'date_of_burial',
            'remarks',
            'client',
            'client_id',  # used for POST/PUT
        ]