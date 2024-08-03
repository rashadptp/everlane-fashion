from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone



class User(AbstractUser):
    SKIN_COLOR_CHOICES = [
        ('FAIR', 'Fair'),
        ('MEDIUM', 'Medium'),
        ('DARK', 'Dark'),
    ]

    HEIGHT_CHOICES = [
        ('SHORT', 'Short'),
        ('MEDIUM', 'Medium'),
        ('TALL', 'Tall'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    SEASON_CHOICES = [
        ('SUMMER', 'Summer'),
        ('WINTER', 'Winter'),
        ('MONSOON', 'Monsoon'),
        ('AUTUMN', 'Autumn'),
    ]

    USAGE_CHOICES = [
        ('CASUAL', 'Casual'),
        ('FORMAL', 'Formal'),
        ('SPORTS', 'Sports'),
        ('PARTY', 'Party'),
    ]
    

    mobile = models.IntegerField(null=True, blank=True)
    skin_color = models.CharField(max_length=10, choices=SKIN_COLOR_CHOICES, null=True, blank=True)
    height = models.CharField(max_length=10, choices=HEIGHT_CHOICES, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    preferred_season = models.CharField(max_length=10, choices=SEASON_CHOICES, null=True, blank=True)
    usage_of_dress = models.CharField(max_length=10, choices=USAGE_CHOICES, null=True, blank=True)
    is_admin=models.BooleanField(default='False')

    def __str__(self):
        return self.username
    

class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category/')
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    image=models.ImageField(upload_to='subcategories/',null=True)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subcategory = models.ForeignKey(Subcategory, related_name='products', on_delete=models.CASCADE)
    image =models.ImageField(upload_to='products/',null=True)
    is_trending=models.BooleanField(default='False')
    summer=models.BooleanField(default='False')
    winter=models.BooleanField(default='False')
    rainy=models.BooleanField(default='False')
    autumn=models.BooleanField(default='False')
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class ProductItem(models.Model):
    SIZES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
    
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    size = models.CharField(max_length=2, choices=SIZES)
    stock = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.product.name} - {self.get_size_display()}"

class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, related_name='wishlists', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='wishlists', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}'s wishlist"


class Cart(models.Model):
    user = models.ForeignKey(User, related_name='carts', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}'s cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.cart.user.username}'s cart"
    
#banner model
from django.db import models

class Banner(models.Model):
    image = models.ImageField(upload_to='banners/')
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.image.url






