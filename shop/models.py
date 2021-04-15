import abc
from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH
from django.urls import reverse

# Create your models here.

class Product(models.Model):

    # Name of the product
    name = models.CharField(max_length=500)

    # Price of the product
    price= models.IntegerField(default=99)

    # Description of the product
    description = models.TextField(blank=True,max_length=1000)

    #Image of the product
    image = models.ImageField(upload_to = 'images/',blank = True)

    # def get_absolute_url(self):
    #     return reverse("product", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.name








