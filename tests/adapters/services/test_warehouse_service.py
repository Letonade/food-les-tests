import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_les_tests.settings')
django.setup()

import pytest
from core.models.locations.customer_basket import CustomerBasketProduct
from core.models.locations.website import WebsiteProduct
from application.services.warehouse_service import WarehouseService
from core.models.locations.product_palette import ProductPalette
from core.models.product import Product
from core.models.warehouse import Warehouse
from core.models.stock_movement_log import StockMovementLog
from tests.fixtures.fixtures import (create_warehouse, create_product, create_palette,
                                     create_customer_basket, create_website, populate_movements)

@pytest.mark.django_db
class TestWarehouseService:

    @pytest.fixture(autouse=True)
    def setup(self, create_warehouse, create_product, create_palette, create_customer_basket, create_website):
        self.warehouse00 = create_warehouse()
        self.warehouse01 = create_warehouse(name='Warehouse01')

        self.productCola = create_product()
        self.productFanta = create_product(name='Fanta')

        self.palette_a = create_palette(
            warehouse=self.warehouse00,
            product=self.productCola,
            name="P001"
        )
        self.palette_b = create_palette(
            warehouse=self.warehouse00,
            product=self.productCola,
            name="P002",
        )
        self.customer_basket_a = create_customer_basket(
            warehouse=self.warehouse00,
            name="CB001"
        )
        self.website_a = create_website(
            warehouse=self.warehouse00,
            name="W001",
        )

    def test_move_product_success(self):
        WarehouseService.move_product(self.palette_a.product, self.palette_a, self.palette_b, 50)

        self.palette_a.refresh_from_db()
        self.palette_b.refresh_from_db()

        assert self.palette_a.quantity == 50
        assert self.palette_b.quantity == 150
        assert self.palette_b.product == self.palette_a.product

        movement_log = StockMovementLog.objects.get(from_location=self.palette_a.name, to_location=self.palette_b.name)
        assert movement_log.quantity == 50
        assert movement_log.movement_type == 'MOVE'

    def test_move_product_to_website(self):
        WarehouseService.move_product(self.palette_a.product, self.palette_a, self.website_a, 50)

        self.palette_a.refresh_from_db()
        self.website_a.refresh_from_db()

        assert self.palette_a.quantity == 50
        website_a_products = WebsiteProduct.objects.get(website=self.website_a, product=self.website_a.products.get(name='Coca Cola'))
        assert website_a_products.quantity == 50

        movement_log = StockMovementLog.objects.get(from_location=self.palette_a.name, to_location=self.website_a.name)

        assert movement_log.quantity == 50
        assert movement_log.movement_type == 'MOVE'

    def test_move_product_to_customer_basket(self):
        WarehouseService.move_product(self.palette_a.product, self.palette_a, self.customer_basket_a, 50)

        self.palette_a.refresh_from_db()
        self.customer_basket_a.refresh_from_db()

        assert self.palette_a.quantity == 50
        customer_basket_a_products = CustomerBasketProduct.objects.get(basket=self.customer_basket_a, product=self.customer_basket_a.products.get(name='Coca Cola'))
        assert customer_basket_a_products.quantity == 50

        movement_log = StockMovementLog.objects.get(from_location=self.palette_a.name, to_location=self.customer_basket_a.name)

        assert movement_log.quantity == 50
        assert movement_log.movement_type == 'MOVE'

    def test_move_product_from_customer_basket_to_palette(self):
        WarehouseService.move_product(self.palette_a.product, self.palette_a, self.customer_basket_a, 50)
        WarehouseService.move_product(self.palette_a.product, self.customer_basket_a, self.palette_a, 20)

        self.palette_a.refresh_from_db()
        self.customer_basket_a.refresh_from_db()

        assert self.palette_a.quantity == 70
        customer_basket_a_products = CustomerBasketProduct.objects.get(basket=self.customer_basket_a, product=self.customer_basket_a.products.get(name='Coca Cola'))
        assert customer_basket_a_products.quantity == 30

        movement_log = StockMovementLog.objects.get(from_location=self.customer_basket_a.name, to_location=self.palette_a.name)

        assert movement_log.quantity == 20
        assert movement_log.movement_type == 'MOVE'

    def test_move_product_from_website_to_palette(self):
        WarehouseService.move_product(self.palette_a.product, self.palette_a, self.website_a, 50)
        WarehouseService.move_product(self.palette_a.product, self.website_a, self.palette_a, 20)

        self.palette_a.refresh_from_db()
        self.website_a.refresh_from_db()

        assert self.palette_a.quantity == 70
        website_a_products = WebsiteProduct.objects.get(website=self.website_a, product=self.website_a.products.get(name='Coca Cola'))
        assert website_a_products.quantity == 30

        movement_log = StockMovementLog.objects.get(from_location=self.website_a.name, to_location=self.palette_a.name)

        assert movement_log.quantity == 20
        assert movement_log.movement_type == 'MOVE'

    def test_move_product_insufficient_stock(self):
        with pytest.raises(ValueError, match="Insufficient stock in the source ProductPalette."):
            WarehouseService.move_product(self.palette_a.product, self.palette_a, self.palette_b, 150)

    def test_move_product_to_occupied_location(self, create_product):
        other_product = create_product(name='Sprite')

        self.palette_b.product = other_product
        self.palette_b.quantity = 30
        self.palette_b.save()

        with pytest.raises(ValueError, match="ProductPalette 'P002' can only contain one kind of product."):
            WarehouseService.move_product(self.palette_a.product, self.palette_a, self.palette_b, 20)

    def test_get_stock_levels(self):
        stock_levels = WarehouseService.get_stock_levels(self.warehouse00)
        assert stock_levels[self.palette_a.name+"_"+self.palette_a.product.name] == 100
        assert stock_levels[self.palette_b.name+"_"+self.palette_b.product.name] == 100

    def test_database_state_before_reset(self, create_warehouse, create_palette, populate_movements):
        warehouse_test = create_warehouse(name='Warehouse_Test')
        palette_a_test = create_palette(warehouse=warehouse_test, name='P100', product=self.productCola)
        palette_b_test = create_palette(warehouse=warehouse_test, name='P101', product=self.productFanta)
        populate_movements(from_location=palette_a_test, to_location=palette_b_test)

        palette_a_test.quantity = 20
        palette_a_test.save()

        palette_a_test.refresh_from_db()
        palette_b_test.refresh_from_db()

        print("\n------------")
        print("Warehouses:", list(Warehouse.objects.values()))
        print("Locations:", list(ProductPalette.objects.values()))
        print("Products:", list(Product.objects.values()))
        print("Movements:", list(StockMovementLog.objects.values()))

        print("Stock Levels in Warehouse_test:", WarehouseService.get_stock_levels(warehouse_test))
        print("------------\n")

        assert StockMovementLog.objects.count() > 0
        assert palette_a_test.quantity == 20
        assert palette_b_test.quantity == 100

