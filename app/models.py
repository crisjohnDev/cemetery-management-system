from django.db import models

# Client / Owner
class Client(models.Model):
    PAYMENT_SCHEMES = [
        ('Full Payment', 'Full Payment'),
        ('Installments', 'Installments'),
    ]

    name = models.CharField(max_length=255)
    lot_number = models.CharField(max_length=50)
    payment_scheme = models.CharField(max_length=20, choices=PAYMENT_SCHEMES)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def amount_paid(self):
        """Calculate total amount paid by the client"""
        return sum(p.amount for p in self.payments.all())

    @property
    def remaining_balance(self):
        """Calculate remaining balance"""
        return self.total_price - self.amount_paid



# Installment schedule (if client chooses installments)
class Installment(models.Model):
    client = models.ForeignKey(Client, related_name='installments', on_delete=models.CASCADE)
    installment_number = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.client.name} - Installment {self.installment_number}"


# Payment record
class Payment(models.Model):
    client = models.ForeignKey(Client, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    installment = models.ForeignKey(Installment, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.client.name} - {self.amount} on {self.date.strftime('%Y-%m-%d')}"


# Burial record
class BurialRecord(models.Model):
    deceased_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)  # optional
    date_of_death = models.DateField()
    date_of_burial = models.DateField()
    remarks = models.TextField(blank=True)
    client = models.ForeignKey(Client, related_name='burial_records', on_delete=models.CASCADE)

    def __str__(self):
        return self.deceased_name
