from django.db import models
from .product import Product
from .locations.product_palette import ProductPalette

class StockMovementLog(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Stock Entry'),
        ('OUT', 'Stock Exit'),
        ('MOVE', 'Internal Movement'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    from_location = models.CharField(max_length=100, null=True, blank=True)
    to_location = models.CharField(max_length=100, null=True, blank=True)
    from_location_type = models.CharField(max_length=100, null=True, blank=True)
    to_location_type = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    movement_type = models.CharField(max_length=5, choices=MOVEMENT_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From: {self.from_location} -> To: {self.to_location} | {self.timestamp} | {self.product.name} | {self.movement_type} | {self.quantity}"
