from django.db import models
from consultasapi.api.validators import validate_date
from django.contrib.auth import get_user_model


class Especialidade(models.Model):
    nome = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.nome


class Medico(models.Model):
    nome = models.CharField(max_length=20)
    crm = models.CharField(max_length=20)
    email = models.CharField(max_length=30, blank=True)
    telefone = models.CharField(max_length=11, blank=True)
    especialidade = models.ForeignKey(Especialidade, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self) -> str:
        return self.nome


class Horario(models.Model):
    horario = models.TimeField()
    ocupado = models.BooleanField()

    def __str__(self) -> str:
        return f'{self.horario}'


class Agenda(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT)
    dia = models.DateField(validators=[validate_date])
    horario = models.ManyToManyField(Horario)

    def __str__(self) -> str:
        return f'{self.medico.nome} {self.dia}'

    class Meta:
        unique_together = ('medico', 'dia')


class Consulta(models.Model):
    data_agendamento = models.DateTimeField(auto_now=True)
    paciente = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    horario = models.TimeField()

    def __str__(self) -> str:
        return f'{self.agenda.dia} - {self.horario} - {self.paciente.email}'
