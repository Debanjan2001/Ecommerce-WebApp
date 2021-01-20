import abc
from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH
from django.urls import reverse

# Create your models here.

class Product(models.Model):

    name = models.CharField(max_length=50)
    price= models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse("product", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.name








