from rest_framework import generics, filters
from consultasapi.api import models, serializers
from rest_framework.permissions import IsAuthenticated


class ListEspecialidades(generics.ListAPIView):
    search_fields = ['nome']
    filter_backends = (filters.SearchFilter,)
    serializer_class = serializers.EspecialidadeSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.Especialidade.objects.all()
