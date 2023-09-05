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
    sortno = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICE = (
        ('pending', 'Pending'),
        ('complete', 'Complete'),
        ('reject', 'Rejected'),
    )
    product = models.ManyToManyField(Product, through='OrderItem')
    
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE)
    created_date = models.DateField(auto_now_add=True)
    quantity = models.PositiveIntegerField()
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)  # Add the total field

    def __str__(self):
        return self.product.name

    # Override the save method to calculate and save the total
    def save(self, *args, **kwargs):
        self.total = self.product.price * self.quantity
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)











# Payment start

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
