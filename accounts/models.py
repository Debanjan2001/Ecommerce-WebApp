from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    first_name = models.CharField(max_length=100,blank=True)

    last_name = models.CharField(max_length=100,blank=True)
    
    def set(self,*args, **kwargs):
        self.first_name = kwargs['first_name']
        self.last_name = kwargs['last_name']
      

    # email = models.EmailField( max_length=254)

    # bio = models.TextField()

    def __str__(self):
        return self.user.username

# @@receiver(post_save, sender=Model)
# def _post_save_receiver(sender, **kwargs):
