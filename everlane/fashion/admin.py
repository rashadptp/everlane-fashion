from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import *

from django.contrib import admin
from .models import *
from django.utils.html import format_html
import json

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Banner)
admin.site.register(ProductItem)
admin.site.register(Address)
admin.site.register(Disaster)
admin.site.register(DressDonation)
admin.site.register(PickupLocation)
class CartHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'formatted_cart_data')

    def formatted_cart_data(self, obj):
        try:
            cart_data = json.loads(obj.cart_data)
            return format_html('<pre>{}</pre>', json.dumps(cart_data, indent=4))
        except json.JSONDecodeError:
            return 'Invalid JSON'
    
    formatted_cart_data.short_description = 'Cart Data'

admin.site.register(CartHistory, CartHistoryAdmin)



