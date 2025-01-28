import time

from django.contrib.sites import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models.customer import Customer
from core.models.locations.customer_basket import CustomerBasket, CustomerBasketProduct
from application.services.warehouse_service import WarehouseService

class ProcessPaymentAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = self._validate_request_data(request.data)

            customer = self._get_customer(data['unique_code'])
            total_to_pay = self._calculate_total_to_pay(customer)
            if (customer.balance-total_to_pay) < 0:
                raise ValueError("customer has not enough.")

            payment_successful = self._call_payment_gateway(customer, total_to_pay)

            if payment_successful:
                customer.balance -= total_to_pay
                customer.save()
                WarehouseService.clear_customer_baskets(customer)
                return Response(
                    {"success": f"Payment of {total_to_pay} for {customer.name} was successful. All baskets have been cleared."},
                    status=status.HTTP_200_OK
                )
            else:
                return Response({"error": "Payment failed. Please try again."}, status=status.HTTP_400_BAD_REQUEST)

        except Customer.DoesNotExist:
            return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _validate_request_data(self, data):
        if "unique_code" not in data or not data["unique_code"]:
            raise ValueError("unique_code is required.")
        return {"unique_code": data["unique_code"]}

    def _get_customer(self, unique_code):
        return Customer.objects.get(unique_code=unique_code)

    def _calculate_total_to_pay(self, customer):
        total = 0
        for basket in CustomerBasket.objects.filter(customer=customer):
            for product_location in CustomerBasketProduct.objects.filter(basket_id=basket.id):
                total += product_location.quantity
        return total

    def _call_payment_gateway(self, customer, amount):
        fake_payment_url = "https://external-provider.com/api/refund/"
        payload = {
            "customer_name": customer.name,
            "customer_code": customer.unique_code,
            "amount": amount
        }
        # Fake, why 2 minutes ???? here 3 seconds
        # I also added a balance in my app just for my personnal feelings
        time.sleep(3)
        #response = requests.post(fake_payment_url, json=payload)
        #return response.status_code == 200
        return True

