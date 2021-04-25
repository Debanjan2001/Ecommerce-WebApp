from django.db import models

# Create your models here.

class Product(models.Model):

    # Name of the product
    name = models.CharField(max_length=500)

    # Price of the product
    price= models.FloatField(default=0.0)

    # Description of the product
    description = models.TextField(blank=True,max_length=1000)

    #Image of the product
    image = models.URLField(blank=True,null=True)

    def __str__(self):
        return self.name









