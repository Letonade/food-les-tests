from django.urls import path
from adapters.api.views.move_product_api_view import MoveProductAPIView

urlpatterns = [
    path("move-product/", MoveProductAPIView.as_view(), name="move-product"),
]