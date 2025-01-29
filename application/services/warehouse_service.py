from core.models import Website, CustomerBasket, ProductPalette
from core.models.locations.customer_basket import CustomerBasketProduct
from core.models.locations.location import Location
from core.models.product import Product
from core.models.stock_movement_log import StockMovementLog
from django.db import transaction

class WarehouseService:
    @staticmethod
    @transaction.atomic
    def move_product(product: Product, from_location: Location, to_location: Location, quantity: int):
        """
        Moves a product from one location to another.

        Args:
            product (Product): The product to move.
            from_location (Location): The source location.
            to_location (Location): The destination location.
            quantity (int): The quantity of the product to move.

        Raises:
            ValueError: If the quantity exceeds available stock or if the move violates business rules.
        """
        WarehouseService._validate_locations(from_location, to_location)

        WarehouseService._process_source(product, from_location, quantity)
        WarehouseService._process_destination(product, to_location, quantity)

        WarehouseService._create_movement_log(product, from_location, to_location, quantity)

        return f"Successfully moved {quantity} of '{product.name}' from {from_location.name} to {to_location.name}."

    @staticmethod
    def _validate_locations(from_location: Location, to_location: Location):
        if not from_location or not to_location:
            raise ValueError("Both source and destination locations must be provided.")

        if from_location == to_location:
            raise ValueError("Source and destination locations cannot be the same.")

    @staticmethod
    def _process_source(product: Product, from_location: Location, quantity: int):
        if from_location.type == "PRODUCT_PALETTE":
            WarehouseService._validate_product_palette_source(product, from_location, quantity)
            from_location.quantity -= quantity
            if from_location.quantity == 0:
                from_location.product = None
            from_location.save()
        elif hasattr(from_location, 'products'):
            WarehouseService._validate_multi_product_source(product, from_location, quantity)
        else:
            raise ValueError("Unsupported source location type.")

    @staticmethod
    def _process_destination(product: Product, to_location: Location, quantity: int):
        if to_location.type == "PRODUCT_PALETTE":
            WarehouseService._validate_product_palette_destination(product, to_location)
            to_location.product = product
            to_location.quantity += quantity
            to_location.save()
        elif hasattr(to_location, 'products'):
            WarehouseService._add_to_multi_product_destination(product, to_location, quantity)
        else:
            raise ValueError("Unsupported destination location type.")

    @staticmethod
    def _validate_product_palette_source(product: Product, from_location: Location, quantity: int):
        if from_location.product != product:
            raise ValueError(f"The product '{product.name}' is not available in the source ProductPalette.")

        if from_location.quantity < quantity:
            raise ValueError("Insufficient stock in the source ProductPalette.")

    @staticmethod
    def _validate_multi_product_source(product: Product, from_location: Location, quantity: int):
        """
        Validates and deducts stock for multi-product source locations like Website or CustomerBasket.
        """
        if isinstance(from_location, Website):
            through_model = from_location.products.through
            location_field = "website"
        elif isinstance(from_location, CustomerBasket):
            through_model = from_location.products.through
            location_field = "basket"
        else:
            raise ValueError("Unsupported source location type for multi-product source.")

        from_location_product = through_model.objects.get(
            **{location_field: from_location, "product": product}
        )

        if from_location_product.quantity < quantity:
            raise ValueError("Insufficient stock in the source location.")

        from_location_product.quantity -= quantity
        from_location_product.save()

    @staticmethod
    def _validate_product_palette_destination(product: Product, to_location: Location):
        if to_location.product and to_location.product != product:
            raise ValueError(f"ProductPalette '{to_location.name}' can only contain one kind of product.")

    @staticmethod
    def _add_to_multi_product_destination(product: Product, to_location: Location, quantity: int):
        through_model = to_location.products.through

        if isinstance(to_location, Website):
            location_field = "website"
        elif isinstance(to_location, CustomerBasket):
            location_field = "basket"
        else:
            raise ValueError("Unsupported destination location type.")

        to_location_product, created = through_model.objects.get_or_create(
            **{location_field: to_location, "product": product},
            defaults={"quantity": 0}
        )

        to_location_product.quantity += quantity
        to_location_product.save()

    @staticmethod
    def _create_movement_log(product: Product, from_location: Location, to_location: Location, quantity: int):
        StockMovementLog.objects.create(
            product=product,
            from_location=from_location.name,
            to_location=to_location.name,
            from_location_type=from_location.type,
            to_location_type=to_location.type,
            quantity=quantity,
            movement_type='MOVE'
        )

    @staticmethod
    def get_stock_levels(warehouse):
        stock_levels = {}
        palettes = ProductPalette.objects.filter(warehouse=warehouse)
        customer_baskets = CustomerBasket.objects.filter(warehouse=warehouse)
        websites = Website.objects.filter(warehouse=warehouse)
        for loc in palettes:
            stock_levels[loc.name+"_"+loc.product.name] = loc.quantity
        for loc in customer_baskets:
            for loc_product in loc.products.values():
                stock_levels[loc.name+"_"+loc_product.name] = loc.quantity
        for loc in websites:
            for loc_product in loc.products.values():
                stock_levels[loc.name+"_"+loc_product.name] = loc.quantity
        return stock_levels

    @staticmethod
    @transaction.atomic
    def clear_customer_baskets(customer):
        for basket in CustomerBasket.objects.filter(customer=customer):
            for product_location in CustomerBasketProduct.objects.filter(basket_id=basket.id):
                StockMovementLog.objects.create(
                    product=product_location.product,
                    from_location=basket.name,
                    to_location="PAYMENT",
                    quantity=product_location.quantity,
                    movement_type="PAYMENT"
                )

        CustomerBasketProduct.objects.filter(basket__customer=customer).delete()
        CustomerBasket.objects.filter(customer=customer).delete()