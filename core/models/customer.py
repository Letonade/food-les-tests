from django.db import models
import random

class Customer(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    age = models.PositiveIntegerField()
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    unique_code = models.CharField(max_length=6, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = self._generate_unique_code()
        super().save(*args, **kwargs)

    @staticmethod
    def _generate_unique_code():
        """Generates a unique 6-digit code."""
        while True:
            code = f"{random.randint(100000, 999999)}"
            if not Customer.objects.filter(unique_code=code).exists():
                return code

    def __str__(self):
        return f"{self.name} ({self.unique_code})"

    class Meta:
        ordering = ["name"]
