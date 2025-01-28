import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_les_tests.settings')
django.setup()

from core.models.customer import Customer
from core.models.warehouse import Warehouse
from core.models.product import Product
from core.models.locations.product_palette import ProductPalette
from core.models.locations.customer_basket import CustomerBasket, CustomerBasketProduct
from core.models.locations.website import Website, WebsiteProduct

def create_initial_data():
    warehouse1 = Warehouse.objects.create(name="Warehouse1", address="123 Main Street")
    warehouse2 = Warehouse.objects.create(name="Warehouse2", address="456 Second Avenue")

    coca_cola = Product.objects.create(name="Coca Cola")
    fanta = Product.objects.create(name="Fanta")

    ProductPalette.objects.create(name="Palette1", warehouse=warehouse1, product=None, quantity=0)
    ProductPalette.objects.create(name="Palette2", warehouse=warehouse1, product=fanta, quantity=50)
    ProductPalette.objects.create(name="Palette3", warehouse=warehouse1, product=coca_cola, quantity=100)
    ProductPalette.objects.create(name="Palette4", warehouse=warehouse1, product=coca_cola, quantity=100)

    website1 = Website.objects.create(name="Website1", warehouse=warehouse1)
    WebsiteProduct.objects.create(website=website1, product=coca_cola, quantity=50)
    WebsiteProduct.objects.create(website=website1, product=fanta, quantity=60)


    website2 = Website.objects.create(name="Website2", warehouse=warehouse2)
    WebsiteProduct.objects.create(website=website2, product=coca_cola, quantity=100)

    customer1 = Customer.objects.create(name="Amelie", address="10 Louis", age=30, balance=500)
    customer2 = Customer.objects.create(name="Bunny", address="20 Lenoir", age=40)

    customer_basket1 = CustomerBasket.objects.create(name="AmelieBasket1", warehouse=warehouse1, customer=customer1)
    customer_basket2 = CustomerBasket.objects.create(name="AmelieBasket2", warehouse=warehouse2, customer=customer1)
    customer_basket3 = CustomerBasket.objects.create(name="BunnyBasket1", warehouse=warehouse1, customer=customer2)
    CustomerBasketProduct.objects.create(basket=customer_basket1, product=coca_cola, quantity=10)
    CustomerBasketProduct.objects.create(basket=customer_basket1, product=fanta, quantity=10)
    CustomerBasketProduct.objects.create(basket=customer_basket2, product=coca_cola, quantity=10)
    CustomerBasketProduct.objects.create(basket=customer_basket3, product=fanta, quantity=10)

    print("Initial data created successfully!")

if __name__ == "__main__":
    create_initial_data()