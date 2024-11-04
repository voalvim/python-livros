from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Autor, Livro
from .serializers import AutorSerializer, LivroSerializer
from rest_framework.decorators import action

class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']

    def create(self, request, *args, **kwargs):
        if Autor.objects.filter(nome=request.data.get('nome')).exists():
            return Response({"detail": "Autor já existe."}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)


class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['titulo', 'autor__nome']

    @action(detail=True, methods=['patch'])
    def atualizar_titulo(self, request, pk=None):
        livro = self.get_object()
        livro.titulo = request.data.get('titulo')
        livro.save()
        return Response({'status': 'Título atualizado!'})
