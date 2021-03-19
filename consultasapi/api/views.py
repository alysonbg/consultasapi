from rest_framework import generics, filters
from consultasapi.api import models, serializers
from rest_framework.permissions import IsAuthenticated


class ListEspecialidades(generics.ListAPIView):
    search_fields = ['nome']
    filter_backends = (filters.SearchFilter,)
    serializer_class = serializers.EspecialidadeSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.Especialidade.objects.all()


class ListMedicos(generics.ListAPIView):
    search_fields = ['nome']
    filter_backends = (filters.SearchFilter, )
    serializer_class = serializers.MedicoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = models.Medico.objects.all()
        especialidades = self.request.GET.getlist('especialidade', None)
        if especialidades:
            return queryset.filter(especialidade__in=especialidades)
        return queryset


class ListAgendas(generics.ListAPIView):
    serializer_class = serializers.AgendaSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = models.Agenda.objects.all()
        medicos = self.request.GET.getlist('medico', None)
        especialidades = self.request.GET.getlist('especialidade', None)
        data_inicio = self.request.query_params.get('data_inicio')
        data_fim = self.request.query_params.get('data_fim')

        if medicos:
            queryset = queryset.filter(medico__in=medicos)
        if especialidades:
            queryset = queryset.filter(medico__especialidade__in=especialidades)
        if data_inicio and data_fim:
            queryset = queryset.filter(dia__range=(data_inicio, data_fim))

        return queryset
