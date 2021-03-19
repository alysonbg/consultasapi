from rest_framework import serializers
from consultasapi.api.models import Especialidade, Medico, Agenda, Consulta


class EspecialidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidade
        fields = ['id', 'nome']


class MedicoSerializer(serializers.ModelSerializer):
    especialidade = EspecialidadeSerializer()

    class Meta:
        model = Medico
        fields = ['id', 'crm', 'nome', 'especialidade']


class AgendaSerializer(serializers.ModelSerializer):
    medico = MedicoSerializer()
    horarios = serializers.StringRelatedField(many=True)

    class Meta:
        model = Agenda
        fields = ['id', 'medico', 'dia', 'horarios']


class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        # In case you want to filter out some fields:
        # fields = ('field_A','field_B' )
        fields = '__all__'
        depth = 1