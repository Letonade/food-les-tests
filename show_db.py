import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_les_tests.settings')
django.setup()

from core.models.locations.customer_basket import CustomerBasketProduct
from core.models.customer import Customer
from core.models.locations.website import WebsiteProduct
from core.models import StockMovementLog, Website, CustomerBasket
from core.models.warehouse import Warehouse
from core.models.product import Product
from core.models.locations.product_palette import ProductPalette

def show_all_you_want():
    print("\n------------ Raw datas")
    print("Warehouses:", list(Warehouse.objects.values()))
    print("Locations - PP:", list(ProductPalette.objects.values()))
    print("Locations - WS:", list(WebsiteProduct.objects.values()))
    print("Locations - CB:", list(CustomerBasketProduct.objects.values()))
    print("Products:", list(Product.objects.values()))
    print("Loc No Pr - WS:", list(Website.objects.values()))
    print("Loc No Pr - CB:", list(CustomerBasket.objects.values()))
    print("Customers:", list(Customer.objects.values()))
    print("Movements:", list(StockMovementLog.objects.values()))
    print("------------ Movement logs\n")
    for movement in StockMovementLog.objects.values():
        print("+n°"+str(movement['id'])+" Type: ["+movement['movement_type']+"]")
        print(": "+movement['from_location']+" -----> "+movement['to_location'])
        product = Product.objects.get(id=movement['product_id'])
        print(": "+product.name+"\t\tat "+movement['timestamp'].strftime("%Y-%m-%d %H:%M:%S"))
        print(": -"+str(movement['quantity'])+"        +"+str(movement['quantity']))
    print("------------ Stocks\n")
    for warehouse in Warehouse.objects.values():
        print(warehouse['name'])
        locations_inspector(ProductPalette.objects.values(), warehouse, 'PP')
        locations_inspector(Website.objects.values(), warehouse, 'WS')
        locations_inspector(CustomerBasket.objects.values(), warehouse, 'CB')
    print("------------ Customers")
    for customer in Customer.objects.values():
        print(f"[{customer['unique_code']}]: {customer['name']} {customer['age']}ans address: {customer['address']} ({customer['balance']})")
    print("------------")

def locations_inspector(objects, warehouse, type):
    for location in objects:
        if warehouse['id'] == location['warehouse_id']:
            print("--  " + location['name'])
            if type == 'WS':
                for l_product in WebsiteProduct.objects.values():
                    if l_product['website_id'] == location['id'] and 'product_id' in l_product and l_product['product_id']:
                        try:
                            product = Product.objects.get(id=l_product['product_id'])
                            print("----  " + product.name + " Q: " + str(l_product['quantity']))
                        except Product.DoesNotExist:
                            print("----  Produit introuvable Q: " + str(l_product['quantity']))
                    else:
                        if l_product['website_id'] == location['id']:
                            print("----  Aucun produit associé à ce website Q: " + str(l_product['quantity']))
            if type == 'CB':
                for l_product in CustomerBasketProduct.objects.values():
                    if l_product['basket_id'] == location['id'] and 'product_id' in l_product and l_product['product_id']:
                        try:
                            product = Product.objects.get(id=l_product['product_id'])
                            print("----  " + product.name + " Q: " + str(l_product['quantity']))
                        except Product.DoesNotExist:
                            print("----  Produit introuvable Q: " + str(l_product['quantity']))
                    else:
                        if l_product['basket_id'] == location['id']:
                            print("----  Aucun produit associé à ce basket Q: " + str(l_product['quantity']))
            if type == 'PP':
                if 'product_id' in location and location['product_id']:
                    try:
                        product = Product.objects.get(id=location['product_id'])
                        print("----  " + product.name + " Q: " + str(location['quantity']))
                    except Product.DoesNotExist:
                        print("----  Produit introuvable Q: " + str(location['quantity']))
                else:
                    print("----  Aucun produit associé à cette palette Q: " + str(location['quantity']))

if __name__ == "__main__":
    show_all_you_want()