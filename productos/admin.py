from django.contrib import admin
from .models import Hamburguesa, Ingrediente

# Register your models here.

admin.site.register(Hamburguesa)
admin.site.register(Ingrediente)