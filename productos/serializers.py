from rest_framework import serializers
from .models import Hamburguesa, Ingrediente


class HamburguesaSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = Hamburguesa
        fields = ("id", "nombre", "precio", "descripcion", "imagen", "ingredientes")
        extra_kwargs = {'ingredientes': {'required': False}}

class IngredienteSerializer(serializers.ModelSerializer):

    class Meta:
        ordering = ['-id']
        model = Ingrediente
        fields = ("id", "nombre", "descripcion")
