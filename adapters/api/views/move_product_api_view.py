from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from application.services.warehouse_service import WarehouseService
from core.models.product import Product
from core.models.locations.product_palette import ProductPalette
from core.models.locations.website import Website
from core.models.locations.customer_basket import CustomerBasket

class MoveProductAPIView(APIView):
    """API view to move products from one location to another."""

    def post(self, request, *args, **kwargs):
        product_name = request.data.get("product_name")
        from_location_name = request.data.get("from_location_name")
        from_location_type = request.data.get("from_location_type")
        to_location_name = request.data.get("to_location_name")
        to_location_type = request.data.get("to_location_type")
        quantity = request.data.get("quantity")

        if not all([product_name, from_location_name, from_location_type, to_location_name, to_location_type, quantity]):
            return Response(
                {"error": "All fields (product_name, from_location_name, from_location_type, to_location_name, to_location_type, quantity) are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            product = Product.objects.get(name=product_name)

            from_location = self._get_location_instance(from_location_name, from_location_type)
            to_location = self._get_location_instance(to_location_name, to_location_type)

            WarehouseService.move_product(product, from_location, to_location, int(quantity))

            return Response({"success": "Product moved successfully."}, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        except (ProductPalette.DoesNotExist, Website.DoesNotExist, CustomerBasket.DoesNotExist):
            return Response({"error": "One or both locations not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _get_location_instance(self, location_name, location_type):
        """Resolve a location instance based on its name and type."""
        if location_type == "PRODUCT_PALETTE":
            return ProductPalette.objects.get(name=location_name)
        elif location_type == "WEBSITE":
            return Website.objects.get(name=location_name)
        elif location_type == "CUSTOMER_BASKET":
            return CustomerBasket.objects.get(name=location_name)
        else:
            raise ValueError(f"Unsupported location type: {location_type}")
