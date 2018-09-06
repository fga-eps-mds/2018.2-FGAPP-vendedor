from django.db import models

# Create your models here.
class Product(models.Model):
    created = models.DateTimeField(auto_now_add= True)
    title = models.CharField(max_length = 50, blank = False)
    description = models.TextField()
    price = models.DecimalField(max_digits= 5, decimal_places= 2, default= '000.00')

    class Meta:
        ordering = ('created',)
