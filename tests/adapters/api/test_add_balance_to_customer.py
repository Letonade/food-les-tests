import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_les_tests.settings')
django.setup()

import pytest
from rest_framework.test import APIClient
from rest_framework import status
from core.models.customer import Customer

@pytest.mark.django_db
class TestAddBalanceToCustomerAPIView:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(name="Alice", address="Wonderland", age=30, balance=0.00, unique_code="123456")

    def test_add_balance_success(self):
        response = self.client.post(
            "/api/add-to-balance/",
            {"unique_code": self.customer.unique_code, "amount": 50},
            format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        self.customer.refresh_from_db()
        assert self.customer.balance == 50.00
        assert "Added 50 to Alice's balance" in response.data["success"]

    def test_add_balance_customer_not_found(self):
        response = self.client.post(
            "/api/add-to-balance/",
            {"unique_code": "000000", "amount": 50.00},
            format="json"
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Customer not found." in response.data["error"]

    def test_add_balance_invalid_amount(self):
        response = self.client.post(
            "/api/add-to-balance/",
            {"unique_code": self.customer.unique_code, "amount": -10.00},
            format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Amount must be a positive number." in response.data["error"]

    def test_add_balance_missing_fields(self):
        response = self.client.post(
            "/api/add-to-balance/",
            {"unique_code": self.customer.unique_code},
            format="json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "amount is required." in response.data["error"]
