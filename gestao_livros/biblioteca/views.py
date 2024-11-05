from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Autor, Livro
from .serializers import AutorSerializer, LivroSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, DjangoModelPermissions
from datetime import datetime, timedelta

class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome']

    def create(self, request, *args, **kwargs):
        if Autor.objects.filter(nome=request.data.get('nome')).exists():
            return Response({"detail": "Autor já existe."}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)


class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['titulo', 'autor__nome']

    @action(detail=True, methods=['patch'])
    def atualizar_titulo(self, request, pk=None):
        livro = self.get_object()
        livro.titulo = request.data.get('titulo')
        livro.save()
        return Response({'status': 'Título atualizado!'})

    @action(detail=False, methods=['get'])
    def publicados_ultimo_ano(self, request):
        um_ano_atras = datetime.now() - timedelta(days=365)
        livros = Livro.objects.filter(data_publicacao__gte=um_ano_atras)
        serializer = self.get_serializer(livros, many=True)
        return Response(serializer.data)
