from django.core.management.base import BaseCommand
from fashion.models import Product
import json

class Command(BaseCommand):
    help = 'Clean and normalize product data'

    def handle(self, *args, **kwargs):
        # Get valid gender choices from the model
        valid_genders = dict(Product.GENDER_CHOICES).keys()

        for product in Product.objects.all():
            # Clean skin_colors
            if isinstance(product.skin_colors, str):
                try:
                    product.skin_colors = json.loads(product.skin_colors)
                except json.JSONDecodeError:
                    product.skin_colors = {}
            
            # Clean heights
            if isinstance(product.heights, str):
                try:
                    product.heights = json.loads(product.heights)
                except json.JSONDecodeError:
                    product.heights = {}

            # Clean usages
            if isinstance(product.usages, str):
                try:
                    product.usages = json.loads(product.usages)
                except json.JSONDecodeError:
                    product.usages = {}

            # Clean gender
            if product.genders not in valid_genders:
                product.genders = None  # Or set to a default valid choice

            if product.genders is None:
                # Set a default gender if needed, e.g., 'U' for Unisex
                product.genders = 'U'

            product.save()

        self.stdout.write(self.style.SUCCESS('Successfully cleaned product data'))
