from rest_framework import viewsets, status
from .serializers import HamburguesaSerializer, IngredienteSerializer
from .models import Hamburguesa, Ingrediente
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def ingrediente_list(request, format=None):
    if request.method == 'GET':
        ingrediente = Ingrediente.objects.all()
        serializer = IngredienteSerializer(ingrediente, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = IngredienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response('Input invalido', status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def ingrediente_detail(request, id):
    try:
        int(id)
    except:
        if request.method == 'GET':
            return Response("id invalido", status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            return Response("ingrediente inexistente", status=status.HTTP_404_NOT_FOUND)

    try:
        ingrediente = Ingrediente.objects.get(id=id)
    except Ingrediente.DoesNotExist:
        return Response("ingrediente inexistente", status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = IngredienteSerializer(ingrediente)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        if len(ingrediente.hamburguesas.all()):
            return Response('Ingrediente no se puede borrar, se encuentra presente en una hamburguesa'
            ,status=status.HTTP_409_CONFLICT)
        else:
            ingrediente.delete()
            return Response('ingrediente eliminado',status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def hamburguesa_list(request, format=None):
    if request.method == 'GET':
        hamburguesa = Hamburguesa.objects.all()
        serializer = HamburguesaSerializer(hamburguesa, many=True)
        for burger in serializer.data:
            n = 0
            for ingrediente in burger['ingredientes']:
                burger['ingredientes'][n] = dict(path='https://hamburgueseria.com/ingrediente/{}'.format(ingrediente))
                n += 1
            data2 = {'id': burger['id']}
            data2.update(burger)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = HamburguesaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response('input invalido', status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE', 'PATCH'])
def hamburguesa_detail(request, id):

    try:
        int(id)
    except:
        if request.method == 'GET':
            return Response("id invalido", status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            return Response("hamburguesa inexistente", status=status.HTTP_404_NOT_FOUND)
        elif request.method == 'PATCH':
            return Response("Parámetros inválidos", status=status.HTTP_400_BAD_REQUEST)
    try:
        hamburguesa = Hamburguesa.objects.get(id=id)
    except Hamburguesa.DoesNotExist:
        return Response("Hamburguesa inexistente", status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = HamburguesaSerializer(hamburguesa)
        n = 0
        for ingrediente in serializer.data['ingredientes']:
            serializer.data['ingredientes'][n] = dict(path='https://hamburgueseria.com/ingrediente/{}'.format(ingrediente))
            n += 1
        data = {'id': hamburguesa.id}
        data.update(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        hamburguesa.delete()
        return Response('hamburguesa eliminada',status=status.HTTP_200_OK)

    elif request.method == 'PATCH':
        if 'ingredientes' in request.data or 'id' in request.data:
            return Response("Parámetros inválidos", status=status.HTTP_400_BAD_REQUEST)
        
        serializer = HamburguesaSerializer(hamburguesa, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            n = 0
            for ingrediente in serializer.data['ingredientes']:
                serializer.data['ingredientes'][n] = dict(path='https://hamburgueseria.com/ingrediente/{}'.format(ingrediente))
                n += 1
            data = {'id': hamburguesa.id}
            data.update(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT', 'DELETE'])
def ingrediente_hamburguesa(request, id_hamburguesa, id_ingrediente):
    try:
        int(id_hamburguesa)
    except:
        return Response("Id de hamburguesa inválido", status = status.HTTP_400_BAD_REQUEST)
    
    try:
        int(id_ingrediente)
    except:
        return Response("Ingrediente inexistente", status = status.HTTP_404_NOT_FOUND)

    try:
        ingrediente = Ingrediente.objects.get(id = id_ingrediente)
    except Ingrediente.DoesNotExist:
        return Response("Ingrediente inexistente", status = status.HTTP_404_NOT_FOUND)
    
    try:
        hamburguesa = Hamburguesa.objects.get(id = id_hamburguesa)
    except:
        return Response("Id de hamburguesa inválido", status = status.HTTP_400_BAD_REQUEST)

    if request.method == "PUT":
        hamburguesa.ingredientes.add(id_ingrediente)
        return Response('Ingrediente agregado', status=status.HTTP_201_CREATED)

    elif request.method == "DELETE":
        serializer = HamburguesaSerializer(hamburguesa)
        if int(id_ingrediente) in serializer.data['ingredientes']:
                hamburguesa.ingredientes.remove(id_ingrediente)
                return Response('ingrediente retirado', status=status.HTTP_200_OK)
        else:
            return Response('Ingrediente inexistente en la hamburguesa', status=status.HTTP_404_NOT_FOUND)