from django.db import models
from uuid import uuid4
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        SELLER = "SELLER", "Seller"
        BUYER = "BUYER", "Buyer"

    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    role = models.CharField(max_length=20, choices=Role.choices)
    phone = models.CharField(max_length=20)
    dp = CloudinaryField("image", folder="Users", blank=True, null=True ,max_length=255)

    def __str__(self):
        return self.username



class Product(models.Model):
    class Category(models.TextChoices):
        ELECTRONICS = "ELECTRONICS", "Electronics"
        FASHION = "FASHION", "Fashion"
        BOOKS = "BOOKS", "Books"
        HOME = "HOME", "Home & Kitchen"
        TOYS = "TOYS", "Toys & Games"
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=Category.choices, default=Category.ELECTRONICS , null = True , blank=True)
    image = CloudinaryField("image", folder="Products", blank=True, null=True ,max_length=255)

    def __str__(self):
        return self.name



class Cart(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    buyer = models.OneToOneField(User, on_delete=models.CASCADE, related_name="carts")

    def total_price(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"{self.buyer.username}'s Cart"


class CartItem(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"



class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        SHIPPED = "SHIPPED", "Shipped"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELLED = "CANCELLED", "Cancelled"

    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    def total_price(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.price_at_purchase

    def __str__(self):
        
        return f"{self.product.name} x {self.quantity}"



class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"

    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    buyer = models.ForeignKey(User , on_delete=models.CASCADE , related_name="payment" , null=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    transaction_id = models.CharField(max_length=200, blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Payment for Order {self.order.id}"



class Review(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.buyer.username} for {self.product.name}"
