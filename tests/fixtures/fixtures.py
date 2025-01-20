from typing import Optional

import pytest
from core.models.product import Product
from core.models.locations.product_palette import ProductPalette
from core.models.locations.location import Location
from core.models.warehouse import Warehouse
from core.models.stock_movement_log import StockMovementLog


@pytest.fixture
def create_warehouse():
    """Fixture factory pour créer un entrepôt avec des paramètres optionnels."""
    def _create_warehouse(name: Optional[str] = None, address: Optional[str] = None) -> Warehouse:
        name = name or "Warehouse00"
        address = address or "8 rue Louis"
        return Warehouse.objects.create(name=name, address=address)
    return _create_warehouse


@pytest.fixture
def create_product():
    def _create_product(name: Optional[str] = None) -> Product:
        name = name or "Coca Cola"
        return Product.objects.create(name=name)
    return _create_product


@pytest.fixture
def create_palette(create_warehouse, create_product):
    def _create_palette(name: Optional[str] = None,
                        warehouse: Optional[Warehouse] = None,
                        product: Optional[Product] = None,
                        quantity: Optional[int] = None) -> ProductPalette:
        name = name or "P001"
        warehouse = warehouse or create_warehouse()
        product = product or create_product()
        quantity = quantity if quantity is not None else 100
        palette = ProductPalette.objects.create(
            name=name,
            warehouse=warehouse,
            product=product,
            quantity=quantity
        )
        return palette
    return _create_palette


@pytest.fixture
def populate_movements(create_palette):
    def _populate_movements(from_location: Optional[Location] = None,
                            to_location: Optional[Location] = None):
        from_location = from_location or create_palette()
        to_location = to_location or create_palette(name="P002")
        StockMovementLog.objects.create(
            product=from_location.product,
            from_location=from_location,
            to_location=to_location,
            from_location_type=from_location.type,
            to_location_type=to_location.type,
            quantity=50,
            movement_type='MOVE'
        )
    return _populate_movements

@pytest.fixture(autouse=True)
def flush_db():
    from django.core.management import call_command
    call_command('flush', '--noinput')