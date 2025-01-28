from django.db import models
from .location import Location
from core.models.product import Product
from .. import Warehouse


class ProductPalette(Location):
    type = "PRODUCT_PALETTE"

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name='product_palettes'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='product_palettes'
    )
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.product.name if self.product else 'Empty'} ({self.quantity})"
