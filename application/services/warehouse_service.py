from django.db import transaction
from core.models.product import Product
from core.models.locations.product_palette import ProductPalette
from core.models.stock_movement_log import StockMovementLog

class WarehouseService:
    @staticmethod
    @transaction.atomic
    def move_product(product: Product, from_location: ProductPalette, to_location: ProductPalette, quantity: int):
        if from_location.product != product:
            raise ValueError("Le produit à déplacer ne correspond pas au produit de l'emplacement source.")
        if to_location.product and to_location.product != product:
            raise ValueError("L'emplacement de destination contient déjà un autre produit.")
        if from_location.quantity < quantity:
            raise ValueError("La quantité demandée dépasse le stock disponible.")

        to_location.product = product
        from_location.quantity -= quantity
        to_location.quantity += quantity
        from_location.save()
        to_location.save()

        StockMovementLog.objects.create(
            product=product,
            from_location=from_location,
            to_location=to_location,
            from_location_type=from_location.type,
            to_location_type=to_location.type,
            quantity=quantity,
            movement_type='MOVE'
        )

    @staticmethod
    def get_stock_levels(warehouse):
        stock_levels = {}
        palettes = ProductPalette.objects.filter(warehouse=warehouse)
        for palette in palettes:
            stock_levels[palette.name] = palette.quantity
        return stock_levels
