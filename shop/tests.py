from django.test import TestCase
from .models import Product
# Create your tests here.

class AnimalTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name = "NFS",price = 250,description = "A Game")

    def test_animals_can_speak(self):
        prod = Product.objects.get(name="NFS")
        self.assertEqual(prod.get_description(), "A Game")
