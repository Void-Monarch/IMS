from django.db import models

from users.models import User


class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=120, unique=True)
    product_unit = models.CharField(max_length=12)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICE = (
        ('pending', 'Pending'),
        ('complete', 'Complete'),
        ('reject', 'Rejected'),
    )

    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE)
    created_date = models.DateField(auto_now_add=True)
    total = models.FloatField(default=0)  # Add the total field

    def __str__(self):
        return str(self.id)


class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.IntegerField(default=1)

    @property
    def get_total_bill(self):
        total = float(self.product.price) * float(self.amount)
        return total


class Payment(models.Model):

    STATUS_CHOICE = (
        ('pending', 'Pending'),
        ('complete', 'Complete'),
        ('reject', 'Rejected'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    card_number = models.PositiveIntegerField(
        max_length=16)  # Adjust this according to your needs
    # Adjust this according to your needs
    holder = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"
