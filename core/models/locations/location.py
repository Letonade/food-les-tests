from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)
    warehouse = models.ForeignKey('core.Warehouse', on_delete=models.CASCADE, related_name='locations')
    type = models.CharField(max_length=50, editable=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
