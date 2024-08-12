from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator


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
    

    mobile = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex='^\d{0,15}$',
                message='Mobile number must be numeric and can contain up to 15 digits',
                code='invalid_mobile_number'
            ),
        ]
    )
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
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    image=models.ImageField(upload_to='subcategories/',null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Product(models.Model):
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand=models.CharField(null=True, max_length=50)
    subcategory = models.ForeignKey(Subcategory, related_name='products', on_delete=models.CASCADE)
    image =models.ImageField(upload_to='products/',null=True)
    is_trending=models.BooleanField(default='False')
    summer=models.BooleanField(default='False')
    winter=models.BooleanField(default='False')
    rainy=models.BooleanField(default='False')
    autumn=models.BooleanField(default='False')
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)


    skin_colors = models.CharField(max_length=255, blank=True)  # e.g., "Fair,Dark"
    heights = models.CharField(max_length=255, blank=True)       # e.g., "Short,Tall"
    genders = models.CharField(max_length=255, blank=True)       # e.g., "M,F"
    usages = models.CharField(max_length=255, blank=True)

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
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
    ]

    PAYMENT_METHODS = [
        ('COD', 'Cash on Delivery'),
        ('ONLINE', 'Online Payment'),
    ]

    


    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)
    is_completed = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS,default='COD')
    payment_status = models.CharField(max_length=20, default='Pending')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')


    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
      
class OrderItem(models.Model):
    RETURN_STATUS_CHOICES = [
        ('NO_RETURN', 'No Return'),
        ('PENDING', 'Return Pending'),
        ('APPROVED', 'Return Approved'),
        ('REJECTED', 'Return Rejected'),
    ]
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


    is_returned = models.BooleanField(default=False)
    return_reason = models.TextField(null=True, blank=True)
    return_requested_on = models.DateTimeField(null=True, blank=True)

    return_status = models.CharField(max_length=10, choices=RETURN_STATUS_CHOICES, default='NO_RETURN')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    refund_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, related_name='wishlists', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='wishlists', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.product.name} in {self.user.username}'s wishlist"


class Cart(models.Model):
    user = models.ForeignKey(User, related_name='carts', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username}'s cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.cart.user.username}'s cart"
    
#banner model
from django.db import models

class Banner(models.Model):
    VIEW = [
        ('A', 'Angular'),
        ('F', 'Flutter'),
    ]
    image = models.ImageField(upload_to='banners/')
    category = models.ForeignKey(Category, related_name='banners', on_delete=models.CASCADE,null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)
    which = models.CharField(max_length=2, choices=VIEW)
    

    def __str__(self):
        return self.image.url

#address list model

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    mobile = models.CharField(max_length=15)
    pincode = models.CharField(max_length=10)
    locality = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not Address.objects.filter(user=self.user).exists():
            self.is_default = True
        elif self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super(Address, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.address}, {self.city}, {self.state}, {self.pincode}'


        













########################################                    DONATION    ###############################################
class Disaster(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='disasters', on_delete=models.CASCADE,null=True)
    created_on = models.DateTimeField(default=timezone.now)

    required_men_dresses = models.IntegerField(default=0)
    required_women_dresses = models.IntegerField(default=0)
    required_kids_dresses = models.IntegerField(default=0)

    fulfilled_men_dresses = models.IntegerField(default=0)
    fulfilled_women_dresses = models.IntegerField(default=0)
    fulfilled_kids_dresses = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def update_fulfillment(self, men_dresses, women_dresses, kids_dresses):
        self.fulfilled_men_dresses += men_dresses
        self.fulfilled_women_dresses += women_dresses
        self.fulfilled_kids_dresses += kids_dresses
        self.save()

    @property
    def is_fulfilled(self):
        return (
            self.fulfilled_men_dresses >= self.required_men_dresses and
            self.fulfilled_women_dresses >= self.required_women_dresses and
            self.fulfilled_kids_dresses >= self.required_kids_dresses
        )


class DressDonation(models.Model):
    user = models.ForeignKey(User, related_name='donations', on_delete=models.CASCADE)
    disaster = models.ForeignKey(Disaster, related_name='donations', on_delete=models.CASCADE)
    men_dresses = models.IntegerField(default=0)
    women_dresses = models.IntegerField(default=0)
    kids_dresses = models.IntegerField(default=0)
    images = models.ImageField(upload_to='donations/', null=True)
    created_on = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.disaster.update_fulfillment(
            self.men_dresses,
            self.women_dresses,
            self.kids_dresses,
        )

    def __str__(self):
        return f"{self.user.username} - {self.disaster.name}"