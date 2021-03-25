from datetime import date
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
    dia = serializers.DateField(source='agenda.dia', read_only=True)
    medico = MedicoSerializer(source='agenda.medico', read_only=True)
    agenda_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Consulta
        fields = ['id', 'dia', 'horario', 'data_agendamento', 'medico', 'agenda_id']
        read_only_fields = ('id', 'dia', 'data_agendamento', 'medico')

    def create(self, validated_data):
        agenda = Agenda.objects.get(id=validated_data['agenda_id'])
        horario = validated_data['horario']
        usuario = self.context['request'].user

        consulta = Consulta.objects.get(agenda=agenda, horario=horario)
        consulta.ocupado = True
        consulta.paciente = usuario
        consulta.save()

        return consulta

    def validate(self, data):
        agenda = Agenda.objects.get(id=data['agenda_id'])
        horario = data['horario']
        paciente = self.context['request'].user
        consultas_marcadas_no_dia = Consulta.objects.filter(paciente=paciente, horario=horario)
        consulta_desejada = Consulta.objects.get(agenda=agenda, horario=horario)
        if agenda.dia < date.today():
            raise serializers.ValidationError('Não é possível marcar consultas para dias passados')

        if len(consultas_marcadas_no_dia) > 0:
            raise serializers.ValidationError('O paciente já possui uma consulta marcada no dia')

        if not consulta_desejada.ocupado:
            raise serializers.ValidationError('Horário já foi marcado por outra pessoa')

        return data



