from django.urls import path
from .views import (
    ClientListCreateView,
    ClientDetailView,
    BurialRecordListCreateView,
    BurialRecordDetailView,
    InstallmentListView,
    InstallmentDetailView,
    PaymentListCreateView,
    PaymentDetailView,
    AddPaymentView,
    ClientByLotView,
    OccupiedLotsView
)

urlpatterns = [
    # === Clients ===
    path('clients/', ClientListCreateView.as_view(), name='client-list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('clients/<int:pk>/add_payment/', AddPaymentView.as_view(), name='client-add-payment'),
    
    path('clients/lot/<str:lot_number>/', ClientByLotView.as_view(), name='client-by-lot'),
    path('cemetery/clients/occupied-lots/', OccupiedLotsView.as_view(), name='occupied-lots'),


    # === Burial Records ===
    path('burial-records/', BurialRecordListCreateView.as_view(), name='burial-record-list'),
    path('burial-records/<int:pk>/', BurialRecordDetailView.as_view(), name='burial-record-detail'),

    # === Installments ===
    path('installments/', InstallmentListView.as_view(), name='installment-list'),
    path('installments/<int:pk>/', InstallmentDetailView.as_view(), name='installment-detail'),

    # === Payments ===
    path('payments/', PaymentListCreateView.as_view(), name='payment-list'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
]
