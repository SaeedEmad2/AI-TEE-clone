from django.db import models
from django.contrib.auth.models import User
class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_size = models.CharField(max_length=50)
    product_color = models.CharField(max_length=50)
    product_price = models.DecimalField(max_digits=10 , decimal_places=2)
    product_image = models.ImageField(upload_to='images/')
    
    def __self__ (self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} * {self.product.product_name}"
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete= models.SET_NULL , null= True , blank= True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

class Shipment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipment')
    ship_status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'), ('in_transit', 'In Transit'),
        ('delivered', 'Delivered')], default='pending')
    
    def __str__(self):
        return f"Shipment for order {self.order.id}"

class Payment(models.Model):
    PAYMENT_CHOICES= [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('cod', 'Cash on Delivery')
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
        ]
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add= True)
    
    def __str__(self):
        return f"Payment for Order {self.order.id}"



    
    
    