from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models import ProductPalette, Website
from core.models.product import Product
from core.models.warehouse import Warehouse
from core.models.locations.customer_basket import CustomerBasket, CustomerBasketProduct
from core.models.customer import Customer
from application.services.warehouse_service import WarehouseService

class MoveProductToBasketAPIView(APIView):
    """
    API view to move a product from any location to a customer's basket if able otherwise create a basket for fullfilement.
    """

    def post(self, request, *args, **kwargs):
        try:
            data = self._validate_request_data(request.data)

            customer = self._get_customer(data['unique_code'])
            product = self._get_product(data['product_name'])
            warehouse = self._get_warehouse(data['warehouse_name'])

            from_location = self._get_location(data['from_location_name'], data['from_location_type'])

            if from_location.warehouse != warehouse:
                raise ValueError(f"{data['from_location_name']} is not part of {data['warehouse_name']}")

            customer_basket = self._get_or_create_customer_basket(customer, warehouse)
            WarehouseService.move_product(product, from_location, customer_basket, data['quantity'])

            return Response(
                {"success": f"Moved {data['quantity']} of '{product.name}' from {from_location.name} to {customer.name}'s basket in {warehouse.name}."},
                status=status.HTTP_200_OK
            )

        except (Customer.DoesNotExist, Product.DoesNotExist, Warehouse.DoesNotExist) as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _validate_request_data(self, data):
        required_fields = ["unique_code", "product_name", "warehouse_name", "from_location_name", "from_location_type"]
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"{field} is required.")

        quantity = data.get("quantity", 1)
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")

        return {
            "unique_code": data["unique_code"],
            "product_name": data["product_name"],
            "warehouse_name": data["warehouse_name"],
            "from_location_name": data["from_location_name"],
            "from_location_type": data["from_location_type"],
            "quantity": quantity
        }

    def _get_customer(self, unique_code):
        return Customer.objects.get(unique_code=unique_code)

    def _get_product(self, product_name):
        return Product.objects.get(name=product_name)

    def _get_warehouse(self, warehouse_name):
        return Warehouse.objects.get(name=warehouse_name)

    def _get_location(self, location_name, location_type):
        location_model = {
            "PRODUCT_PALETTE": ProductPalette,
            "WEBSITE": Website,
            "CUSTOMER_BASKET": CustomerBasket
        }.get(location_type)

        if not location_model:
            raise ValueError(f"Unsupported location type: {location_type}")

        location = location_model.objects.filter(name=location_name).first()
        if not location:
            raise ValueError(f"Location with name '{location_name}' and type '{location_type}' not found.")

        return location

    def _get_or_create_customer_basket(self, customer, warehouse):
        customer_basket = CustomerBasket.objects.filter(customer=customer, warehouse=warehouse).first()
        if not customer_basket:
            customer_basket = CustomerBasket.objects.create(
                name=f"Basket_{customer.name}_{warehouse.name}",
                customer=customer,
                warehouse=warehouse
            )
        return customer_basket
