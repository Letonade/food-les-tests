import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_les_tests.settings')
django.setup()

import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.core.management import call_command
from core.models.product import Product
from core.models.locations.product_palette import ProductPalette
from core.models.warehouse import Warehouse

@pytest.mark.django_db
def test_move_product_with_names_api():
    # Flush the database before running the test
    call_command('flush', '--noinput')

    # Setup initial data
    warehouse = Warehouse.objects.create(name="Warehouse1", address="123 Main Street")
    product = Product.objects.create(name="Coca Cola")
    from_palette = ProductPalette.objects.create(name="PaletteA", warehouse=warehouse, product=product, quantity=100)
    to_palette = ProductPalette.objects.create(name="PaletteB", warehouse=warehouse, product=None, quantity=0)

    # Create a test user
    # User.objects.create_user(username="testuser", password="testpassword")

    # Create API client
    client = APIClient()
    # client.login(username="testuser", password="testpassword")

    # Perform the API request
    response = client.post(
        "/api/move-product/",
        {
            "product_name": "Coca Cola",
            "from_location_name": "PaletteA",
            "to_location_name": "PaletteB",
            "quantity": 50,
        },
        format="json",
    )

    # Assertions
    assert response.status_code == 200
    assert response.data["success"] == "Product moved successfully."

    # Verify database state
    from_palette.refresh_from_db()
    to_palette.refresh_from_db()
    assert from_palette.quantity == 50
    assert to_palette.quantity == 50
