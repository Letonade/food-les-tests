from django.urls import path
from adapters.api.views.move_product_api_view import MoveProductAPIView
from adapters.api.views.move_product_to_basket_api_view import MoveProductToBasketAPIView

urlpatterns = [
    path("move-product/", MoveProductAPIView.as_view(), name="move-product"),
    path("move-product-to-basket/", MoveProductToBasketAPIView.as_view(), name="move-product-to-basket"),
]