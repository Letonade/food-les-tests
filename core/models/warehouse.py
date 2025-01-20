from django.db import models

class Warehouse(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._temp_locations = []  # Temporary list for internal processing

    def __str__(self):
        return self.name

    def get_locations(self):
        return self.locations.all()

    def total_stock(self):
        return sum(location.quantity for location in self.get_locations() if hasattr(location, 'quantity'))
