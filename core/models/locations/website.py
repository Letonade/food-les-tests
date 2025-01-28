from django.db import models
from .location import Location
from core.models.product import Product

class Website(Location):
    type = "WEBSITE"

    warehouse = models.ForeignKey(
        'core.Warehouse',
        on_delete=models.CASCADE,
        related_name='websites'
    )
    products = models.ManyToManyField(
        Product,
        through='WebsiteProduct',
        related_name='websites'
    )

    def __str__(self):
        return f"Website: {self.name} ({self.warehouse.name})"


class WebsiteProduct(models.Model):
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name="website_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("website", "product")

    def __str__(self):
        return f"{self.website.name} - {self.product.name}: {self.quantity}"
