from django.db import models
from .location import Location
from core.models.product import Product

class CustomerBasket(Location):
    type = "CUSTOMER_BASKET"

    warehouse = models.ForeignKey(
        'core.Warehouse',
        on_delete=models.CASCADE,
        related_name='customer_baskets'
    )
    products = models.ManyToManyField(
        Product,
        through='CustomerBasketProduct',
        related_name='customer_baskets'
    )

    def __str__(self):
        return f"Customer Basket: {self.name} ({self.warehouse.name})"


class CustomerBasketProduct(models.Model):
    basket = models.ForeignKey(CustomerBasket, on_delete=models.CASCADE, related_name="basket_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("basket", "product")

    def __str__(self):
        return f"{self.basket.name} - {self.product.name}: {self.quantity}"
