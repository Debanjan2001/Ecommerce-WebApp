from django.utils import timezone
from shop.models import Product
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    first_name = models.CharField(max_length=100,blank=True,default='')

    last_name = models.CharField(max_length=100,blank=True,default='')

    activation_date = models.DateTimeField(blank=True,default=timezone.now)
    
    products = models.ManyToManyField(Product,blank=True)

    def set(self,*args, **kwargs):
        self.first_name = kwargs['first_name']
        self.last_name = kwargs['last_name']
        self.activation_date = timezone.now()


    def __str__(self):
        return self.user.username

# @@receiver(post_save, sender=Model)
# def _post_save_receiver(sender, **kwargs):
