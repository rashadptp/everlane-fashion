from django.contrib import admin
from .models import *

from django.utils.html import format_html
import json

class CartHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'formatted_cart_data')

    def formatted_cart_data(self, obj):
        try:
            cart_data = json.loads(obj.cart_data)
            return format_html('<pre>{}</pre>', json.dumps(cart_data, indent=4))
        except json.JSONDecodeError:
            return 'Invalid JSON'
    
    formatted_cart_data.short_description = 'Cart Data'