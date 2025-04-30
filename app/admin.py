from django.contrib import admin
from .models import Product  # ✅ correction ici

admin.site.register(Product)