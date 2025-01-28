import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_les_tests.settings')
django.setup()

import pytest
from rest_framework.test import APIClient
from rest_framework import status
from core.models.product import Product
from core.models.warehouse import Warehouse
from core.models.locations.product_palette import ProductPalette
from core.models.locations.website import Website, WebsiteProduct
from core.models.locations.customer_basket import CustomerBasket, CustomerBasketProduct
from core.models.customer import Customer


@pytest.mark.django_db
class TestMoveProductToBasketAPIView:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()

        self.warehouse = Warehouse.objects.create(name="Warehouse1", address="123 Main Street")
        self.warehouse2 = Warehouse.objects.create(name="Warehouse2", address="124 Main Street")

        self.customer = Customer.objects.create(name="Alice", address="Wonderland", age=30)

        self.product_cola = Product.objects.create(name="Coca Cola")
        self.product_fanta = Product.objects.create(name="Fanta")

        self.palette = ProductPalette.objects.create(
            name="Palette1", warehouse=self.warehouse, product=self.product_cola, quantity=100
        )
        self.palette2 = ProductPalette.objects.create(
            name="Palette2", warehouse=self.warehouse2, product=self.product_cola, quantity=100
        )

    def test_move_product_to_existing_basket(self):
        customer_basket = CustomerBasket.objects.create(
            name="AliceBasket", warehouse=self.warehouse, customer=self.customer
        )

        response = self.client.post(
            "/api/move-product-to-basket/",
            {
                "unique_code": self.customer.unique_code,
                "product_name": self.product_cola.name,
                "warehouse_name": self.warehouse.name,
                "from_location_name": self.palette.name,
                "from_location_type": "PRODUCT_PALETTE",
                "quantity": 50
            },
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        self.palette.refresh_from_db()
        assert self.palette.quantity == 50  # Reduced in the source
        basket_product = CustomerBasketProduct.objects.get(basket=customer_basket, product=self.product_cola)
        assert basket_product.quantity == 50  # Added to the basket

    def test_move_product_creates_new_basket(self):
        assert CustomerBasket.objects.filter(customer=self.customer, warehouse=self.warehouse).count() == 0

        response = self.client.post(
            "/api/move-product-to-basket/",
            {
                "unique_code": self.customer.unique_code,
                "product_name": self.product_cola.name,
                "warehouse_name": self.warehouse.name,
                "from_location_name": self.palette.name,
                "from_location_type": "PRODUCT_PALETTE",
                "quantity": 30
            },
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        self.palette.refresh_from_db()
        assert self.palette.quantity == 70  # Reduced in the source
        customer_basket = CustomerBasket.objects.get(customer=self.customer, warehouse=self.warehouse)
        basket_product = CustomerBasketProduct.objects.get(basket=customer_basket, product=self.product_cola)
        assert basket_product.quantity == 30  # Added to the new basket

    def test_move_product_insufficient_stock(self):
        response = self.client.post(
            "/api/move-product-to-basket/",
            {
                "unique_code": self.customer.unique_code,
                "product_name": self.product_cola.name,
                "warehouse_name": self.warehouse.name,
                "from_location_name": self.palette.name,
                "from_location_type": "PRODUCT_PALETTE",
                "quantity": 200
            },
            format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        self.palette.refresh_from_db()
        assert self.palette.quantity == 100

    def test_move_product_from_invalid_location(self):
        response = self.client.post(
            "/api/move-product-to-basket/",
            {
                "unique_code": self.customer.unique_code,
                "product_name": self.product_cola.name,
                "warehouse_name": self.warehouse.name,
                "from_location_name": "NonExistentPalette",
                "from_location_type": "PRODUCT_PALETTE",
                "quantity": 10
            },
            format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Location with name" in response.data["error"]

    def test_move_product_from_invalid_warehouse(self):
        response = self.client.post(
            "/api/move-product-to-basket/",
            {
                "unique_code": self.customer.unique_code,
                "product_name": self.product_cola.name,
                "warehouse_name": self.warehouse2.name,
                "from_location_name": self.palette.name,
                "from_location_type": "PRODUCT_PALETTE",
                "quantity": 10
            },
            format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Palette1 is not part of Warehouse2" in response.data["error"]

    def test_move_product_with_invalid_customer(self):
        response = self.client.post(
            "/api/move-product-to-basket/",
            {
                "unique_code": "000000",  # Invalid customer code
                "product_name": self.product_cola.name,
                "warehouse_name": self.warehouse.name,
                "from_location_name": self.palette.name,
                "from_location_type": "PRODUCT_PALETTE",
                "quantity": 10
            },
            format="json"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Customer matching query does not exist." in response.data["error"]
