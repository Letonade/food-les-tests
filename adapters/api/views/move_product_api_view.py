from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from application.services.warehouse_service import WarehouseService
from core.models.locations.product_palette import ProductPalette
from core.models.product import Product


class MoveProductAPIView(APIView):
    def post(self, request, *args, **kwargs):
        product_name = request.data.get("product_name")
        from_location_name = request.data.get("from_location_name")
        to_location_name = request.data.get("to_location_name")
        quantity = request.data.get("quantity")

        if not all([product_name, from_location_name, to_location_name, quantity]):
            return Response(
                {"error": "All fields (product_name, from_location_name, to_location_name, quantity) are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            product = Product.objects.get(name=product_name)
            from_location = ProductPalette.objects.get(name=from_location_name)
            to_location = ProductPalette.objects.get(name=to_location_name)

            WarehouseService.move_product(product, from_location, to_location, int(quantity))

            return Response({"success": "Product moved successfully."}, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        except ProductPalette.DoesNotExist:
            return Response({"error": "Location not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An unexpected error occurred: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
