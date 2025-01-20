import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_les_tests.settings')
django.setup()

from core.models import StockMovementLog
from core.models.warehouse import Warehouse
from core.models.product import Product
from core.models.locations.product_palette import ProductPalette

def show_all_you_want():
    print("\n------------")
    for warehouse in Warehouse.objects.values():
        print(warehouse['name'])
        for palette in ProductPalette.objects.values():
            if warehouse['id'] == palette['warehouse_id']:
                print("--  " + palette['name'])
                if palette['product_id']:
                    try:
                        product = Product.objects.get(id=palette['product_id'])
                        print("----  " + product.name + " Q: " + str(palette['quantity']))
                    except Product.DoesNotExist:
                        print("----  Produit introuvable Q: " + str(palette['quantity']))
                else:
                    print("----  Aucun produit associé Q: " + str(palette['quantity']))
    print("------------")

    print("\n------------")
    print("Warehouses:", list(Warehouse.objects.values()))
    print("Locations:", list(ProductPalette.objects.values()))
    print("Products:", list(Product.objects.values()))
    print("Movements:", list(StockMovementLog.objects.values()))
    print("------------\n")

if __name__ == "__main__":
    show_all_you_want()