from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
def __str__(self):
    return self.name

class AccessRight(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    can_view = models.BooleanField(default=False)
    can_add = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)