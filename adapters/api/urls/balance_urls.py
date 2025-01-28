from django.urls import path
from adapters.api.views.add_balance_to_customer_api_view import AddBalanceToCustomerAPIView
from adapters.api.views.process_payment_api_view import ProcessPaymentAPIView

urlpatterns = [
    path("add-to-balance/", AddBalanceToCustomerAPIView.as_view(), name="add-to-balance"),
    path("pay-all/", ProcessPaymentAPIView.as_view(), name="pay-all"),
]