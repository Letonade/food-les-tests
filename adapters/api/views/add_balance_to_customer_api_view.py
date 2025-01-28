from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models.customer import Customer

class AddBalanceToCustomerAPIView(APIView):
    """API view to add balance to a customer's account using their unique code."""

    def post(self, request, *args, **kwargs):
        try:
            data = self._validate_request_data(request.data)

            customer = self._get_customer(data['unique_code'])
            amount = data['amount']

            customer.balance += amount
            customer.save()

            return Response(
                {"success": f"Added {amount} to {customer.name}'s balance. New balance: {customer.balance}"},
                status=status.HTTP_200_OK
            )

        except Customer.DoesNotExist:
            return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _validate_request_data(self, data):
        required_fields = ["unique_code", "amount"]
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"{field} is required.")

        amount = data.get("amount")
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount must be a positive number.")

        return {
            "unique_code": data["unique_code"],
            "amount": amount
        }

    def _get_customer(self, unique_code):
        return Customer.objects.get(unique_code=unique_code)
