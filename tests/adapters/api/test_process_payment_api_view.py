import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_les_tests.settings')
django.setup()

import pytest
from rest_framework.test import APIClient
from rest_framework import status
from core.models.customer import Customer
from core.models.product import Product
from core.models.locations.customer_basket import CustomerBasket, CustomerBasketProduct
from core.models.stock_movement_log import StockMovementLog
from core.models.warehouse import Warehouse

@pytest.mark.django_db
class TestProcessPaymentAPIView:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()

        self.customer = Customer.objects.create(
            name="Alice", address="Wonderland", age=30, balance=100.00, unique_code="123456"
        )

        self.warehouse = Warehouse.objects.create(name="Main Warehouse", address="123 Main Street")

        self.product1 = Product.objects.create(name="Coca Cola")
        self.product2 = Product.objects.create(name="Fanta")

        self.basket1 = CustomerBasket.objects.create(name="AliceBasket1", warehouse=self.warehouse, customer=self.customer)
        CustomerBasketProduct.objects.create(basket=self.basket1, product=self.product1, quantity=10)

        self.basket2 = CustomerBasket.objects.create(name="AliceBasket2", warehouse=self.warehouse, customer=self.customer)
        CustomerBasketProduct.objects.create(basket=self.basket2, product=self.product2, quantity=5)

    def test_process_payment_success(self):
        #I should mock the call to an exterior api, pytest has mocker...
        response = self.client.post(
            "/api/pay-all/",
            {"unique_code": self.customer.unique_code},
            format="json"
        )
        print(f"--------------")
        print(f"--------------")
        print(f"{response=}")
        print(f"{response.data=}")
        print(f"--------------")
        print(f"--------------")

        assert response.status_code == status.HTTP_200_OK
        assert "Payment of 15 for Alice was successful. All baskets have been cleared." in response.data["success"]

        assert CustomerBasket.objects.filter(customer=self.customer).count() == 0
        assert CustomerBasketProduct.objects.filter(basket__customer=self.customer).count() == 0

        logs = StockMovementLog.objects.filter(movement_type="PAYMENT")
        assert logs.count() == 2

        log1 = logs.get(product=self.product1)
        assert log1.from_location == self.basket1.name
        assert log1.to_location == "PAYMENT"
        assert log1.quantity == 10

        log2 = logs.get(product=self.product2)
        assert log2.from_location == self.basket2.name
        assert log2.to_location == "PAYMENT"
        assert log2.quantity == 5

    def test_process_payment_customer_not_found(self):
        response = self.client.post(
            "/api/pay-all/",
            {"unique_code": "000000"},
            format="json"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Customer not found." in response.data["error"]

    def test_process_payment_missing_balance(self):
        self.customer.balance = 0
        self.customer.save()

        response = self.client.post(
            "/api/pay-all/",
            {"unique_code": self.customer.unique_code},
            format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "customer has not enough." in response.data["error"]

    def test_process_payment_missing_unique_code(self):
        response = self.client.post(
            "/api/pay-all/",
            {},
            format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "unique_code is required." in response.data["error"]
