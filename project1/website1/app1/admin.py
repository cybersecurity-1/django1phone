from django.contrib import admin
from .models import Register
from .models import Product,Cart
from .models import Order,Category

admin.site.register(Register)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Category)

# Register your models here.
