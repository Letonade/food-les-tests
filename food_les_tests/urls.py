from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('adapters.api.urls.move_product_urls')),
    path('api/', include('adapters.api.urls.balance_urls')),
]