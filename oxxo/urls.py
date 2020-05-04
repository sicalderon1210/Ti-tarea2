from django.contrib import admin
from django.urls import path, include
from productos.views import  *
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
 
# Routers provide an easy way of automatically determining the URL conf.



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('ingrediente', ingrediente_list),
    path('ingrediente/<id>', ingrediente_detail),
    path('hamburguesa', hamburguesa_list),
    path('hamburguesa/<id>', hamburguesa_detail),
    path('hamburguesa/<id_hamburguesa>/ingrediente/<id_ingrediente>', ingrediente_hamburguesa)
]
urlpatterns = format_suffix_patterns(urlpatterns)
