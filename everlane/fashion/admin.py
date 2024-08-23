from django.contrib import admin
from .models import *

from django.utils.html import format_html
import json
from .resources import *

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
admin.site.register(CartHistory, CartHistoryAdmin)



