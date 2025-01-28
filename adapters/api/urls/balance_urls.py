from django.urls import path
from adapters.api.views.add_balance_to_customer_api_view import AddBalanceToCustomerAPIView

urlpatterns = [
    path("add-to-balance/", AddBalanceToCustomerAPIView.as_view(), name="add-to-balance"),
]