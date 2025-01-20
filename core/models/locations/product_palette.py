from django.db import models
from .location import Location

class ProductPalette(Location):
    type = "PRODUCT_PALETTE"  # Direct assignment of type

    product = models.ForeignKey('core.Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='product_palettes')
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.product.name if self.product else 'Empty'} ({self.quantity})"
