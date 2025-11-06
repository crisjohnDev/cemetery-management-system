from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Client, BurialRecord, Installment, Payment
from .serializers import (
    ClientSerializer,
    BurialRecordSerializer,
    InstallmentSerializer,
    PaymentSerializer
)

# === Clients ===
class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ClientByLotView(APIView):
    def get(self, request, lot_number):
        try:
            client = Client.objects.get(lot_number=lot_number)
            serializer = ClientSerializer(client)
            return Response(serializer.data)
        except Client.DoesNotExist:
            return Response({"detail": "Lot not found"}, status=404)

# === Burial Records ===
class BurialRecordListCreateView(generics.ListCreateAPIView):
    queryset = BurialRecord.objects.all()
    serializer_class = BurialRecordSerializer

class BurialRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BurialRecord.objects.all()
    serializer_class = BurialRecordSerializer

# === Installments ===
class InstallmentListView(generics.ListAPIView):
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer

class InstallmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer

# === Payments ===
class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

# === Add Payment to a specific client ===
class AddPaymentView(APIView):
    def post(self, request, pk):
        try:
            client = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return Response({"error": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

        amount = request.data.get('amount')
        if not amount:
            return Response({"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = float(amount)
        except ValueError:
            return Response({"error": "Invalid amount"}, status=status.HTTP_400_BAD_REQUEST)

        remaining_balance = float(client.total_price) - float(client.amount_paid)
        if amount > remaining_balance:
            return Response({"error": "Payment exceeds remaining balance"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the payment
        payment = Payment.objects.create(client=client, amount=amount)
        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)

class OccupiedLotsView(APIView):
    def get(self, request):
        # Get all lots that have a client assigned
        lots = Client.objects.exclude(name__isnull=True).values_list('lot_number', flat=True)
        return Response(list(lots))