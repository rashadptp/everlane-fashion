from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import *

from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Banner)



