from django.db import models

class StaffMember(models.Model):
    name = models.CharField(max_length=100)
    paid = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name

